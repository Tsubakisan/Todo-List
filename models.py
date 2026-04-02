from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# データベースインスタンスの作成
db = SQLAlchemy()

# タスクモデルの定義
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    title = db.Column(db.String(100), nullable=False)  # タスクタイトル（必須）
    description = db.Column(db.Text, nullable=True)  # タスク説明（任意）
    due_date = db.Column(db.Date, nullable=True)  # 期限（任意）
    priority = db.Column(db.String(10), default='medium')  # 優先度（デフォルト: medium）
    completed = db.Column(db.Boolean, default=False)  # 完了状態（デフォルト: False）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 作成日時

    def __repr__(self):
        return f'<Task {self.title}>'
