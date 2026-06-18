Here’s a Python script that attaches to a ChatGPT conversation already loaded in Chrome/Edge, scrolls it fully, extracts messages, and saves **Markdown + HTML**.

```bash
pip install playwright beautifulsoup4 markdownify
playwright install chromium
```

Start Chrome/Edge with remote debugging:

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Windows PowerShell
chrome.exe --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222
```

Open the ChatGPT conversation in that browser, then run:

```python
# save_chatgpt_conversation.py
import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.async_api import async_playwright

OUT = Path("chatgpt_conversation_export")
OUT.mkdir(exist_ok=True)

async def scroll_to_top_and_bottom(page):
    # ChatGPT often virtualizes/loads content while scrolling.
    for _ in range(40):
        await page.mouse.wheel(0, -2500)
        await page.wait_for_timeout(150)

    for _ in range(80):
        await page.mouse.wheel(0, 2500)
        await page.wait_for_timeout(150)

async def extract_messages(page):
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")

    # Current-ish ChatGPT message structure. May need adjustment if UI changes.
    candidates = soup.select('[data-message-author-role]')

    messages = []
    for el in candidates:
        role = el.get("data-message-author-role", "unknown").strip()
        text_html = str(el)
        text_md = md(text_html, heading_style="ATX").strip()

        # Cleanup common UI noise
        lines = [
            line.rstrip()
            for line in text_md.splitlines()
            if line.strip() not in {"Copy", "Edit", "Retry", "Share"}
        ]
        clean = "\n".join(lines).strip()

        if clean:
            messages.append((role, clean, text_html))

    return messages

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]

        # Pick the visible ChatGPT tab
        page = None
        for pg in context.pages:
            if "chatgpt.com" in pg.url or "chat.openai.com" in pg.url:
                page = pg
                break

        if page is None:
            raise RuntimeError("No ChatGPT tab found. Open the conversation first.")

        await page.bring_to_front()
        await scroll_to_top_and_bottom(page)

        title = await page.title()
        messages = await extract_messages(page)

        markdown_parts = [f"# {title}\n"]
        html_parts = [f"<h1>{title}</h1>"]

        for i, (role, content_md, content_html) in enumerate(messages, 1):
            markdown_parts.append(f"\n\n## {i}. {role.title()}\n\n{content_md}")
            html_parts.append(
                f"<section><h2>{i}. {role.title()}</h2>{content_html}</section>"
            )

        md_path = OUT / "conversation.md"
        html_path = OUT / "conversation.html"

        md_path.write_text("\n".join(markdown_parts), encoding="utf-8")
        html_path.write_text(
            "<!doctype html><meta charset='utf-8'>\n" + "\n".join(html_parts),
            encoding="utf-8",
        )

        print(f"Saved {len(messages)} messages:")
        print(md_path.resolve())
        print(html_path.resolve())

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run:

```bash
python save_chatgpt_conversation.py
```

This avoids the blank-page PDF problem by extracting the actual conversation DOM instead of relying on browser print/export.
