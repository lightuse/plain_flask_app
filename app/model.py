
import pandas as pd

subjects = {0: '建物の中から撮影したお庭', 1: '外で撮影したお庭', 2: 'お菓子やお抹茶', 3: '洋館の中', 4: '建物の外観', 5: 'その他の写真'}
subject_names = list(subjects.values())
class Subject:
    def list():
        return subjects

    def name(index):
        return subject_names[index]

commenters = {0: '接客スタッフ', 1: '庭師さん', 2: '広報さん', 3: 'マイケルさん', 4: '所長'}
commenter_names = list(commenters.values())
class Comment:
    def __init__(self, commenter_index, subject_index):
        self.commenter_index = commenter_index
        self.subject_index = subject_index

    def commenter_name(self):
        return commenter_names[self.commenter_index]

    def message(self):
        csv_data = 'app/static/csv/comment_' + str(self.commenter_index) + '.csv'
        df = pd.read_csv(csv_data)
        comments = df.query(f'subject == {self.subject_index}')
        comment = comments.sample(n=1)['message']
        return comment.iloc[-1]
