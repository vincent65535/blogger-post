from googleapiclient.discovery import build


class BloggerClient:
    def __init__(self, credentials):
        self.service = build('blogger', 'v3', credentials=credentials)

    def publish_post(self, blog_id, title, content, labels=None, is_draft=False):
        body = {
            'kind': 'blogger#post',
            'title': title,
            'content': content,
        }
        if labels:
            body['labels'] = labels

        request = self.service.posts().insert(
            blogId=blog_id,
            body=body,
            isDraft=is_draft
        )
        return request.execute()
