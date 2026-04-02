from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from forms import TaskForm
from models import db, Task
import os

#Flaskアプリケーションの初期化
from flask import Flask

# Flaskアプリケーションの初期化
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-her'  # セキュリティキー
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # データベースURI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 変更追跡の無効化

# データベースの初期化
db.init_app(app)

# テーブルの作成
with app.app_context():
    db.create_all()

# ホームページ - タスク一覧を表示
@app.route('/')
def index():
    tasks = Task.query.all()  # すべてのタスクを取得
    return render_template('index.html', tasks=tasks)

# タスク追加ページ
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()

    if form.validate_on_submit():  # フォームが送信され、検証に成功した場合
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data
        )
        db.session.add(task)  # タスクをデータベースに追加
        db.session.commit()  # 変更をコミット
        flash('タスクが正常に追加されました！', 'success')  # 成功メッセージ
        return redirect(url_for('index'))  # ホームページにリダイレクト

    return render_template('add_task.html', form=form)

# タスク編集ページ
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)  # タスクを取得、存在しない場合は404エラー

    form = TaskForm(obj=task)  # フォームに既存のタスクデータを設定
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        db.session.commit()  # 変更をコミット
        flash('タスクが正常に更新されました！', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_task.html', form=form, task=task)


# タスク削除機能
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)  # タスクを削除
    db.session.commit()  # 変更をコミット
    flash('タスクが正常に削除されました！', 'success')
    return redirect(url_for('index'))

# タスク完了/未完了切り替え機能
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed # 完了状態を切り替え
    db.session.commit()
    status = "完了" if task.completed else "未完了"
    flash(f'タスクを{status}に設定しました！', 'success')
    return redirect(url_for('index'))

# エラーハンドラー
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404 # 404エラーページを表示

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # データベースのロールバック
    return render_template('500.html'), 500  # 500エラーページを表示

if __name__ == '__main__':
    app.run(debug=True)  # デバッグモードでアプリケーションを実行
