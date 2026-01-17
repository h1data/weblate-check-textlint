# customize/textlint_check.py

from weblate.checks.base import TargetCheck
from customize.textlint.textlint_client import TextlintClient

class TextlintCheck(TargetCheck):
    """ check for a translation unit with textlint """
    default_disabled = True
    check_id = "check_textlint"
    name = "Textlintチェック違反"
    description = "詳細はコメントを参照してください"

    textlintClient = TextlintClient()
    
    def check_single(self, source, target, unit):
        """
        execute textlint from translation unit
        and add comments warnings
        """
    
        try:
            messages = self.textlintClient.lint_text(target or "", unit.translation.language.code)["messages"]

            existed_comments = unit.unresolved_comments
            if not messages or len(messages) == 0:
                for c in existed_comments:
                    try:
                        if c.user.is_bot and c.user.username == "check:textlint":
                            c.resolved = True
                            c.save(update_fields=["resolved"])
                    except Exception:
                        # ignore per-comment errors
                        pass
                return False
            
            # deferred importing ORM class
            from weblate.auth.models import User
            from weblate.trans.models import Comment

            new_comments = []

            for m in messages:
                summary = f"{m['message']} ({m['ruleId']})"
                if not summary in new_comments:
                    new_comments.append(summary)
                    if not self.__has_comment(summary, existed_comments):
                        # add comment if there is no equivalent comment
                        Comment.objects.create(
                            comment = summary,
                            user = User.objects.get_or_create_bot(
                                scope="check",
                                name="textlint",
                                verbose="texlint check",
                            ),
                            unit = unit
                        )
        
            for c in existed_comments:
                if c.user.is_bot and c.user.username == "check:textlint" and not c.comment in new_comments:
                    try:
                        c.resolved = True
                        c.save(update_fields=["resolved"])
                    except Exception:
                        # ignore per-comment errors
                        pass
            return True

        except Exception as e:
            # do nothing for exceptions
            print(f'TextlintCheck ERROR! {e}')
            return False

    def __has_comment(self, text: str, comments: list) -> bool:
        for c in comments:
            if c.comment == text:
                return True
        return False
