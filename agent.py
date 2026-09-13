import re
from urllib.parse import urlparse

from anakin_client import search_web
from ai_client import analyze_opportunities

# Established employers are used as a PRIORITY signal, not a hard requirement.
PREFERRED_COMPANIES = {
    "google", "microsoft", "amazon", "adobe", "atlassian", "nvidia", "ibm",
    "salesforce", "oracle", "sap", "cisco", "intel", "walmart", "qualcomm",
    "uber", "flipkart", "zoho", "phonepe", "razorpay", "swiggy", "zomato",
    "accenture", "deloitte", "ey", "tcs", "infosys", "wipro", "hcl",
    "capgemini", "jpmorgan", "goldman sachs", "morgan stanley", "visa",
    "mastercard", "paypal", "booking.com", "spotify", "siemens", "bosch",
    "samsung", "hp", "dell", "linkedin", "meta", "netflix", "airbnb",
}

TRUSTED_JOB_DOMAINS = (
    "careers.", "jobs.", "greenhouse.io", "lever.co", "myworkdayjobs.com",
    "workday.com", "ashbyhq.com", "linkedin.com", "indeed.com",
    "wellfound.com", "internshala.com"
)

WEAK_AGGREGATOR_DOMAINS = (
    "freshershunt", "freshersworld", "careers360", "jobalert", "jobrapido",
    "talent.com", "jooble", "simplyhired"
)

EXPIRED_PHRASES = [
    "expired", "application closed", "applications closed", "closed for applications",
    "no longer accepting", "not accepting applications", "position filled",
    "role filled", "job no longer available", "opportunity closed",
    "applications are now closed", "deadline has passed", "deadline passed",
    "past deadline", "posting has expired", "this job has expired",
    "job is no longer available", "applications are no longer being accepted",
]


def _combined_text(item):
    return " ".join(
        str(item.get(k, "") or "")
        for k in (
            "title", "company", "snippet", "description", "content", "text",
            "summary", "deadline", "status"
        )
    ).lower()


def _domain(url):
    try:
        return urlparse(str(url)).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def _company_text(item):
    company = item.get("company", "")
    if isinstance(company, dict):
        return str(company.get("name", "") or "")
    return str(company or "")


def detect_status(item):
    text = _combined_text(item)
    if any(p in text for p in EXPIRED_PHRASES):
        return "expired"

    explicit = str(item.get("status", "") or "").lower().strip()
    if explicit in {"closed", "expired"}:
        return explicit
    if explicit in {"active", "open", "accepting applications"}:
        return "active"

    positive = [
        "apply now", "apply today", "applications open", "currently accepting",
        "accepting applications", "open for applications", "apply online",
        "submit application", "internship program"
    ]
    if any(p in text for p in positive):
        return "active"
    return "unknown"


def _source_quality(item):
    domain = _domain(item.get("url", ""))
    text = _combined_text(item)
    score = 0
    label = "Web source"

    if any(domain.endswith(d) or d in domain for d in TRUSTED_JOB_DOMAINS):
        score += 25
        label = "Trusted job source"

    if domain.startswith("careers.") or domain.startswith("jobs."):
        score += 15
        label = "Company careers"

    if "greenhouse.io" in domain or "lever.co" in domain or "ashbyhq.com" in domain or "myworkdayjobs.com" in domain:
        score += 15
        label = "ATS / application platform"

    if any(company in text for company in PREFERRED_COMPANIES):
        score += 25

    if any(domain.endswith(d) or d in domain for d in WEAK_AGGREGATOR_DOMAINS):
        score -= 20
        label = "Aggregator"

    return score, label


def _popular_company_bonus(item):
    text = f"{item.get('title', '')} {_company_text(item)} {item.get('snippet', '')}".lower()
    return 25 if any(company in text for company in PREFERRED_COMPANIES) else 0


def _normalize(raw):
    if not isinstance(raw, dict):
        return None

    title = str(raw.get("title") or raw.get("name") or "").strip()
    url = str(raw.get("url") or raw.get("application_url") or raw.get("link") or "").strip()
    if not title or not url:
        return None

    item = dict(raw)
    item["title"] = title
    item["url"] = url
    item["status"] = detect_status(item)
    source_score, source_label = _source_quality(item)
    item["_source_quality"] = source_score
    item["_source_label"] = source_label
    item["_popular_bonus"] = _popular_company_bonus(item)
    return item


def _dedupe(items):
    seen = set()
    output = []
    for item in items:
        key = str(item.get("url", "")).lower().rstrip("/")
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def _search_queries(profile):
    """Build search intent from the user's actual goal instead of a fixed role."""
    goal = str(profile.get("goal", "internships")).strip()
    skills = ", ".join(profile.get("skills", [])) or "relevant technical skills"
    education = str(profile.get("education", "college student")).strip()
    location = str(profile.get("location", "India / Remote")).strip()

    return [
        f"Find current 2026 opportunities matching this exact target: {goal}. "
        f"Candidate: {education}. Skills: {skills}. Location preference: {location}. "
        "Prioritize live openings and real application pages. Exclude expired or closed roles.",

        f"Find current 2026 {goal} for a college student. "
        f"Candidate education: {education}. Skills: {skills}. Preferred location: {location}. "
        "Prioritize well-known established employers and official company career pages. "
        "Return actual open roles, not articles, career advice, or expired posts.",

        f"Search official careers and reputable ATS/job platforms for current openings for: {goal}. "
        f"Match skills {skills}; candidate is {education}; location {location}. "
        "Prefer company career pages, Greenhouse, Lever, Workday or Ashby. "
        "Avoid stale, closed, duplicate and obviously irrelevant listings.",

        f"Find additional high-quality live opportunities for {goal} in {location}. "
        f"Skills: {skills}. Candidate: {education}. "
        "Favor recognized technology/product companies and verified application links. "
        "Only include roles that appear current; do not return expired or closed opportunities.",
    ]


def _candidate_pool(items):
    # Quality-first pool: active + source/company quality, then unknown live pages.
    return sorted(
        items,
        key=lambda x: (
            1 if x.get("status") == "active" else 0,
            x.get("_source_quality", 0) + x.get("_popular_bonus", 0),
        ),
        reverse=True,
    )[:24]


def _fallback_item(item, profile):
    text = _combined_text(item)
    skills = [s.lower() for s in profile.get("skills", [])]
    matching = [s for s in profile.get("skills", []) if s.lower() in text]

    score = 40
    if "intern" in text or "internship" in text:
        score += 12
    if matching:
        score += min(20, 5 * len(matching))
    if "india" in text or "remote" in text:
        score += 8
    if item.get("status") == "active":
        score += 8
    score += min(12, max(0, item.get("_source_quality", 0)) // 5)
    score = min(score, 92)

    return {
        "title": item.get("title"),
        "url": item.get("url"),
        "company": item.get("company", ""),
        "score": score,
        "eligibility": "medium",
        "matching_skills": matching,
        "missing_requirements": ["Verify exact eligibility on the live application page"],
        "deadline": item.get("deadline", ""),
        "status": item.get("status", "unknown"),
        "action": "PREPARE",
        "reason": "Strong candidate found from live search; review the official listing before applying.",
        "source_label": item.get("_source_label", "Web source"),
    }


def _clean_ai(recommendations):
    cleaned = []
    seen = set()
    for item in recommendations or []:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url", "") or "").strip()
        if not url:
            continue
        text = _combined_text(item)
        if any(p in text for p in EXPIRED_PHRASES):
            continue
        if str(item.get("action", "")).upper() == "SKIP":
            continue
        key = url.lower().rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(item)
    return cleaned


def _enrich_recommendation(item, candidate_by_url):
    url = str(item.get("url", "")).lower().rstrip("/")
    candidate = candidate_by_url.get(url, {})
    if candidate:
        item.setdefault("source_label", candidate.get("_source_label", "Web source"))
        item.setdefault("company", candidate.get("company", ""))
        item["status"] = detect_status({**candidate, **item})
        item["_source_quality"] = candidate.get("_source_quality", 0)
        item["_popular_bonus"] = candidate.get("_popular_bonus", 0)
    return item


def run_applypilot(profile):
    if not profile:
        raise ValueError("Profile is required.")

    queries = _search_queries(profile)
    all_results = []

    # Four focused searches. This gives diversity without repeatedly burning credits.
    for query in queries:
        try:
            data = search_web(query, limit=8)
        except Exception:
            continue

        if isinstance(data, dict):
            results = data.get("results", [])
        elif isinstance(data, list):
            results = data
        else:
            results = []

        for raw in results:
            item = _normalize(raw)
            if item:
                all_results.append(item)

    all_results = _dedupe(all_results)

    viable = [x for x in all_results if x.get("status") not in {"expired", "closed"}]
    candidates = _candidate_pool(viable)

    if not candidates:
        return {
            "recommendations": [],
            "message": "No current opportunities were found for this search target. Try broadening the role, location, or skills.",
            "search_stats": {
                "queries_used": len(queries),
                "raw_results": len(all_results),
                "candidates_analyzed": 0,
                "recommendations_returned": 0,
                "search_strategy": "4 intent-driven Anakin searches × up to 8 results",
            },
        }

    clean_candidates = [
        {k: v for k, v in x.items() if not k.startswith("_")}
        for x in candidates
    ]

    recommendations = []
    try:
        analysis = analyze_opportunities(profile, clean_candidates)
        if isinstance(analysis, dict):
            recommendations = analysis.get("recommendations", [])
        elif isinstance(analysis, list):
            recommendations = analysis
    except Exception:
        recommendations = []

    recommendations = _clean_ai(recommendations)
    candidate_by_url = {
        str(x.get("url", "")).lower().rstrip("/"): x for x in candidates
    }

    enriched = []
    for item in recommendations:
        enriched.append(_enrich_recommendation(dict(item), candidate_by_url))
    recommendations = enriched

    used = {str(x.get("url", "")).lower().rstrip("/") for x in recommendations}

    for candidate in candidates:
        key = str(candidate.get("url", "")).lower().rstrip("/")
        if key in used:
            continue
        recommendations.append(_fallback_item(candidate, profile))
        used.add(key)
        if len(recommendations) >= 8:
            break

    def sort_key(item):
        try:
            match_score = float(item.get("score", 0) or 0)
        except Exception:
            match_score = 0
        status = str(item.get("status", "")).lower()
        source_quality = float(item.get("_source_quality", 0) or 0)
        popular = float(item.get("_popular_bonus", 0) or 0)
        return (
            match_score,
            1 if status == "active" else 0,
            source_quality + popular,
        )

    recommendations.sort(key=sort_key, reverse=True)
    recommendations = recommendations[:8]

    # Never allow an explicit expired/closed signal back into the final cards.
    recommendations = [
        x for x in recommendations
        if detect_status(x) not in {"expired", "closed"}
    ][:8]

    return {
        "recommendations": recommendations,
        "search_stats": {
            "queries_used": len(queries),
            "raw_results": len(all_results),
            "candidates_analyzed": len(candidates),
            "recommendations_returned": len(recommendations),
            "search_strategy": "4 intent-driven Anakin searches × up to 8 results",
        },
    }
