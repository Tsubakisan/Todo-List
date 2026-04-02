from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

# タスクフォームの定義
class TaskForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired()])  # 必須フィールド
    description = TextAreaField('説明', validators=[Optional()])  # 任意フィールド
    due_date = DateField('期限', format='%Y-%m-%d', validators=[Optional()])  # 日付フィールド
    priority = SelectField('優先度', choices=[
        ('low', '低'),
        ('medium', '中'),
        ('high', '高')
    ], default='medium')  # 選択フィールド
    submit = SubmitField('タスクを保存')  # 送信ボタン
