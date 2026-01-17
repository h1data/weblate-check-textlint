from django.utils.html import escape, format_html, format_html_join
from django.utils.translation import gettext, gettext_lazy
from weblate.checks.base import TargetCheck

from customize.textlint.textlint_client import TextlintClient

class TextlintCheck(TargetCheck):
    """ check for a translation unit with textlint """
    default_disabled = True
    check_id = "check_textlint"
    name = "textlintチェック違反"
    description = "textlintチェックエラーがあります"

    textlintClient = TextlintClient()
    
    def check_single(self, source, target, unit):
        """
        execute textlint from translation unit
        and add comments warnings
        """
    
        try:
            messages = self.textlintClient.lint_text(target or "", unit.translation.language.code)["messages"]
            return not (not messages or len(messages) == 0)
        except Exception as e:
            # do nothing for exceptions
            print(f'TextlintCheck ERROR! {e}')
            return False

    def get_description(self, check_obj):
        unit = check_obj.unit
        # Collect target plural forms and run textlint on each
        targets = unit.get_target_plurals()

        summaries = []
        try:
            from weblate.utils.markdown import render_markdown

            for t in targets:
                msgs = self.textlintClient.lint_text(t or "", unit.translation.language.code).get("messages", [])
                for m in msgs:
                    summary = render_markdown(f"{m.get("message", "")} ({m.get("ruleId", "")})")
                    if summary and summary not in summaries:
                        summaries.append(summary)

        except Exception as e:
            # If textlint fails here, return a generic message
            print(f'TextlintCheck ERROR! {e}')
            return format_html(escape("textlintとの連携に失敗しました"))

        if not summaries:
            return super().get_description(check_obj)

        # Build an unordered list of unique summaries
        list_items = format_html_join("\n", "<li>{}</li>", ((s,) for s in summaries))
        return format_html("<ul>{}</ul>", list_items)
