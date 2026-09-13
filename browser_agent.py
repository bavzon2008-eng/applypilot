import os
import asyncio
import re
from urllib.parse import urljoin

from dotenv import load_dotenv
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

load_dotenv()

ANAKIN_API_KEY = os.getenv("ANAKIN_API_KEY")
BROWSER_WS_URL = "wss://api.anakin.io/v1/browser-connect"

APPLICATION_PATTERNS = [
    r"\bapply\b",
    r"\beasy apply\b",
    r"\bstart application\b",
    r"\bstart applying\b",
    r"\bapply on company website\b",
    r"\bcontinue to application\b",
    r"\bcontinue application\b",
    r"\bapplication form\b",
]
APPLICATION_REGEX = re.compile("|".join(APPLICATION_PATTERNS), re.IGNORECASE)

APPLICATION_FIELD_HINTS = [
    "first name", "last name", "full name", "your name", "email", "phone",
    "mobile", "resume", "cv", "cover letter", "linkedin", "portfolio",
    "github", "address", "city", "state", "country", "work authorization",
    "sponsorship", "education", "school", "university", "degree",
    "graduation", "college", "experience", "years of experience",
]

GENERIC_FIELD_EXCLUSIONS = [
    "newsletter", "subscribe", "search", "comment", "message", "contact",
    "login", "sign in", "password", "coupon", "promo", "chat",
]

VERIFICATION_PATTERNS = [
    "additional verification required", "verify you are human", "checking your browser",
    "just a moment", "cloudflare", "captcha", "security check", "robot check",
    "access denied", "verify your identity",
]


def _clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


async def _safe_eval(page, script, arg=None, default=None):
    try:
        return await page.evaluate(script, arg)
    except Exception:
        return default


async def _safe_text(page):
    value = await _safe_eval(
        page,
        """() => document.body ? (document.body.innerText || document.body.textContent || '') : ''""",
        default="",
    )
    return _clean(value)


async def _safe_title(page):
    try:
        return _clean(await page.title(timeout=5000))
    except Exception:
        return ""


def _safe_url(page):
    try:
        return page.url or ""
    except Exception:
        return ""


async def _page_controls(page):
    return await _safe_eval(
        page,
        """() => Array.from(document.querySelectorAll('a,button,[role="button"]')).map(el => ({
            tag: el.tagName.toLowerCase(),
            text: (el.innerText || el.textContent || '').trim(),
            href: el.href || el.getAttribute('href') || '',
            disabled: !!el.disabled
        })).filter(x => x.text)""",
        default=[],
    ) or []


async def _find_apply_control(page):
    controls = await _page_controls(page)
    for control in controls:
        text = _clean(control.get("text"))
        if APPLICATION_REGEX.search(text) and not control.get("disabled"):
            return control
    return None


async def _click_control(page, control):
    """Click a control through DOM JS to avoid brittle Playwright locator waits."""
    text = _clean(control.get("text"))
    href = _clean(control.get("href"))

    # Prefer a real href because it is deterministic and does not depend on a JS click.
    if href:
        return {"clicked": False, "href": href, "method": "href"}

    result = await _safe_eval(
        page,
        """targetText => {
            const nodes = Array.from(document.querySelectorAll('a,button,[role="button"]'));
            const node = nodes.find(el => (el.innerText || el.textContent || '').trim() === targetText);
            if (!node) return false;
            node.click();
            return true;
        }""",
        text,
        default=False,
    )
    return {"clicked": bool(result), "href": "", "method": "js"}


async def _extract_fields(page):
    fields = await _safe_eval(
        page,
        """() => Array.from(document.querySelectorAll('input,textarea,select')).map((el, i) => {
            const type = (el.getAttribute('type') || el.tagName || 'text').toLowerCase();
            const id = el.id || '';
            let label = '';
            if (id) {
                const labelEl = document.querySelector(`label[for="${CSS.escape(id)}"]`);
                if (labelEl) label = labelEl.innerText || '';
            }
            if (!label) {
                const parentLabel = el.closest('label');
                if (parentLabel) label = parentLabel.innerText || '';
            }
            return {
                index: i,
                type: type === 'textarea' ? 'textarea' : type === 'select' ? 'select' : type,
                name: el.getAttribute('name') || '',
                id,
                placeholder: el.getAttribute('placeholder') || '',
                aria_label: el.getAttribute('aria-label') || '',
                label: label.trim()
            };
        }).filter(x => !['hidden','submit','button','reset'].includes(x.type))""",
        default=[],
    ) or []

    relevant = []
    for field in fields:
        haystack = " ".join([
            field.get("name", ""), field.get("id", ""), field.get("placeholder", ""),
            field.get("aria_label", ""), field.get("label", "")
        ]).lower()
        if any(ex in haystack for ex in GENERIC_FIELD_EXCLUSIONS):
            continue
        if any(hint in haystack for hint in APPLICATION_FIELD_HINTS):
            relevant.append(field)

    return relevant


def _verification_blocked(title, text):
    combined = f"{title} {text}".lower()
    return any(pattern in combined for pattern in VERIFICATION_PATTERNS)


def _looks_like_application_page(title, text, fields, current_url):
    combined = f"{title} {text}".lower()
    domain = _clean(current_url).lower()
    application_signals = [
        "application form", "job application", "apply for", "candidate information",
        "submit application", "application questions", "resume upload", "upload resume",
        "cover letter", "work authorization", "years of experience",
    ]
    signal_count = sum(1 for signal in application_signals if signal in combined)
    ats_domain = any(x in domain for x in ["greenhouse.io", "lever.co", "ashbyhq.com", "myworkdayjobs.com", "workday.com"])

    # A genuine form requires multiple relevant fields, or strong application language + at least one field.
    return len(fields) >= 2 and (signal_count >= 1 or ats_domain)


async def inspect_and_open_application_page(url):
    if not ANAKIN_API_KEY:
        raise RuntimeError("ANAKIN_API_KEY is missing from .env")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(
            BROWSER_WS_URL,
            headers={"X-API-Key": ANAKIN_API_KEY},
        )

        try:
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = context.pages[0] if context.pages else await context.new_page()
            navigation_warning = None

            try:
                await page.goto(url, wait_until="commit", timeout=20000)
            except PlaywrightTimeoutError:
                navigation_warning = "The site responded slowly. ApplyPilot continued with the page state that was available."
            except Exception as exc:
                navigation_warning = f"The site could not fully load: {str(exc)[:180]}"

            await page.wait_for_timeout(1200)

            original_url = _safe_url(page)
            original_title = await _safe_title(page)
            original_text = await _safe_text(page)

            if _verification_blocked(original_title, original_text):
                screenshot = None
                try:
                    screenshot = await page.screenshot(type="png", full_page=False)
                except Exception:
                    pass
                return {
                    "success": True,
                    "original_url": original_url,
                    "original_title": original_title,
                    "apply_control_found": False,
                    "apply_control_text": "",
                    "application_page_opened": False,
                    "real_application_form": False,
                    "agent_status": "VERIFICATION_BLOCKED",
                    "title": original_title,
                    "url": original_url,
                    "page_text": original_text[:6000],
                    "buttons": [],
                    "links": [],
                    "application_keywords": [],
                    "form_keywords": [],
                    "form_fields": [],
                    "submitted": False,
                    "navigation_warning": navigation_warning,
                    "verification_detected": True,
                    "verification_reason": "The destination is protected by an anti-bot or verification step.",
                    "screenshot": screenshot,
                }

            controls = await _page_controls(page)
            apply_control = await _find_apply_control(page)
            apply_found = bool(apply_control)
            application_page_opened = False
            application_navigation_url = ""

            if apply_control:
                click_info = await _click_control(page, apply_control)
                href = click_info.get("href", "")

                if href:
                    application_navigation_url = urljoin(original_url, href)
                    try:
                        await page.goto(application_navigation_url, wait_until="commit", timeout=20000)
                        application_page_opened = True
                    except PlaywrightTimeoutError:
                        application_page_opened = True
                        navigation_warning = "The Apply destination responded slowly; ApplyPilot inspected the available page state."
                    except Exception:
                        application_page_opened = False
                elif click_info.get("clicked"):
                    application_page_opened = True
                    await page.wait_for_timeout(1800)

            # Some Apply buttons open a new tab.
            if apply_found and not application_page_opened and len(context.pages) > 1:
                try:
                    page = context.pages[-1]
                    await page.wait_for_timeout(1200)
                    application_page_opened = True
                except Exception:
                    pass

            final_url = _safe_url(page)
            final_title = await _safe_title(page)
            final_text = await _safe_text(page)

            if _verification_blocked(final_title, final_text):
                screenshot = None
                try:
                    screenshot = await page.screenshot(type="png", full_page=False)
                except Exception:
                    pass
                return {
                    "success": True,
                    "original_url": original_url,
                    "original_title": original_title,
                    "apply_control_found": apply_found,
                    "apply_control_text": _clean((apply_control or {}).get("text", "")),
                    "application_page_opened": application_page_opened,
                    "real_application_form": False,
                    "agent_status": "VERIFICATION_BLOCKED",
                    "title": final_title,
                    "url": final_url,
                    "page_text": final_text[:6000],
                    "buttons": [x.get("text", "") for x in controls if x.get("tag") == "button"][:50],
                    "links": [x.get("text", "") for x in controls if x.get("tag") == "a"][:50],
                    "application_keywords": [],
                    "form_keywords": [],
                    "form_fields": [],
                    "submitted": False,
                    "navigation_warning": navigation_warning,
                    "verification_detected": True,
                    "verification_reason": "The application destination requires anti-bot or security verification.",
                    "screenshot": screenshot,
                }

            form_fields = await _extract_fields(page)
            real_form = _looks_like_application_page(final_title, final_text, form_fields, final_url)

            if real_form:
                agent_status = "APPLICATION_READY"
            elif application_page_opened:
                agent_status = "APPLICATION_PAGE_OPENED"
            elif apply_found:
                agent_status = "APPLICATION_CONTROL_FOUND"
            elif final_text:
                agent_status = "OPPORTUNITY_ONLY"
            else:
                agent_status = "BLOCKED"

            form_keywords = [
                keyword for keyword in [
                    "resume", "cv", "cover letter", "email", "phone", "first name",
                    "last name", "education", "linkedin", "github", "application"
                ] if keyword in final_text.lower()
            ]

            screenshot = None
            try:
                screenshot = await page.screenshot(type="png", full_page=False)
            except Exception:
                pass

            return {
                "success": True,
                "original_url": original_url,
                "original_title": original_title,
                "apply_control_found": apply_found,
                "apply_control_text": _clean((apply_control or {}).get("text", "")),
                "application_page_opened": application_page_opened,
                "real_application_form": real_form,
                "agent_status": agent_status,
                "title": final_title,
                "url": final_url,
                "application_navigation_url": application_navigation_url,
                "page_text": final_text[:6000],
                "buttons": [x.get("text", "") for x in controls if x.get("tag") == "button"][:50],
                "links": [x.get("text", "") for x in controls if x.get("tag") == "a"][:50],
                "application_keywords": form_keywords,
                "form_keywords": form_keywords,
                "form_fields": form_fields[:30] if real_form else [],
                "submitted": False,
                "navigation_warning": navigation_warning,
                "verification_detected": False,
                "verification_reason": "",
                "screenshot": screenshot,
            }
        finally:
            await browser.close()


def inspect_and_open_application(url):
    return asyncio.run(inspect_and_open_application_page(url))


def inspect_application(url):
    return inspect_and_open_application(url)
