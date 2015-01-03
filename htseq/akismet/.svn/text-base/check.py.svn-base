import akismet
import settings

akismet.USERAGENT = "SequencerMap/1.0"

def check_akismet(request, comment):
    site = request.META.get('HTTP_HOST', settings.WEBSITE_URL)
    try:
        real_key = akismet.verify_key(settings.AKISMET_KEY, site)
        if real_key:
            is_spam = akismet.comment_check(settings.AKISMET_KEY,
                site,
                request.META.get('REMOTE_ADDR', '127.0.0.1'),
                request.META.get('HTTP_USER_AGENT', 'unknown'),
                comment_content=comment)
            if is_spam:
                return True
            else:
                return False
    except akismet.AkismetError, e:
        print e.response, e.statuscode
    return None

# If you're a good person, you can report false positives via
# akismet.submit_ham(), and false negatives via akismet.submit_spam(),
# using exactly the same parameters as akismet.comment_check().

