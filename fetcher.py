import re
import zulip


def remove_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text


class ZulipFetcher:
    def __init__(self, config_file):
        self.client = zulip.Client(config_file=config_file)

    def fetch_messages(self, count):
        result = []

        # Get newest messages
        request: dict[str, any] = {
            "anchor": "newest",
            "num_before": count,
            "num_after": 0,
        }

        # Send request
        request_result = self.client.get_messages(request)

        # Format request
        messages = request_result['messages']
        for msg in messages:
            clean_msg = remove_html_tags(msg['content'])

            result.append([msg['sender_full_name'], clean_msg, msg['id']])

        return result
