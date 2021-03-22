# qPost
Basic Q&A board that allows users to ask questions and allows others to answer them. The main idea of this would be for classes. Students can submit a question and other students who know the answer would be able to answer it, the teacher would curate the answers or answer themselves.

Stack - MySQL database, Flask backend, HTML,CSS,Javascript, Bootstrap 5.0

Basic Features
- Login system, with password hashing and salting.
- Ask a question.
- Answer a question.
- Mark answers to your questions.
- View all questions.
- Delete only your questions or answers to your questions.
- Teachers can manage all questions and answers.

Learned
- Flask Blueprints and app factory design pattern.
- more in-depth Jinja templating.
- Handling login sessions and session verification through decorators.
- Salting and hashing passwords.

Future Todo
- Filters for types of questions, unanswered questions.
- Page for completed questions.
- Stats of users for teachers.
- Dynamic pages vs reload after data changes using JS.
- Improve UI. Make it look like a post it board where questions look like post it notes. Students can customize look of post it note, and can place at a location on the page.
- Dockerize Flask project with required compoonents.
