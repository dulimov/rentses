from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_admin import Admin, AdminIndexView
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
import pymysql
import logging
import os
import enum
from logging.handlers import RotatingFileHandler
from flask_migrate import Migrate
from datetime import datetime, date
from flask_mail import Message, Mail
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from flask_login import LoginManager, login_required
from flask_babel import Babel, gettext as _
from sqlalchemy.orm import relationship
from flask_admin.form import ImageUploadField
from sqlalchemy import Column, Integer, String, ForeignKey
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import Form, FileField, FieldList
from wtforms import FieldList, FormField
from wtforms.fields import Field as BaseField
from flask_admin.model.form import InlineFormAdmin
from wtforms.fields import SelectField
from wtforms import Field
from flask_admin.form import RenderTemplateWidget





# Замена MySQLdb на pymysql
pymysql.install_as_MySQLdb()

# Создание экземпляра приложения Flask
app = Flask(__name__, template_folder='www/templates')
app = Flask(__name__, static_url_path='/', static_folder='static')


# Установка конфигурации соединения с базой данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://:@localhost/care_es'
app.config['SECRET_KEY'] = 'dwdw44dfdsf4eed'

babel = Babel(app)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


 
# Определение модели User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return f"<User {self.username}>"
        
# Настройка логгера для Flask-Admin
admin_logger = logging.getLogger('admin')
admin_logger.setLevel(logging.INFO)
handler = RotatingFileHandler('flask-admin.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
admin_logger.addHandler(handler)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Переопределение базового класса AdminIndexView для добавления логирования
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # Здесь можно добавить проверку аутентификации и авторизации
        return True

    def inaccessible_callback(self, name, **kwargs):
        # Метод для редиректа пользователя, если он не авторизован
        return redirect(url_for('login', next=request.url))

    def _handle_view(self, name, **kwargs):
        """
        Этот метод переопределяется для добавления логирования при каждом доступе к админ-панели.
        """
        admin_logger.info(f'Страница админки "{name}" была запрошена.')
        return super(MyAdminIndexView, self)._handle_view(name, **kwargs)

# Инициализация Flask-Admin с переопределенным представлением
admin = Admin(app, index_view=MyAdminIndexView(), name='MyApp', template_mode='bootstrap3')

# Определение представления в админке для модели User
class UserView(ModelView):
    pass
    
# Определение мулььзагрузет    
class MultiImageField(BaseField):
    widget = RenderTemplateWidget('MultiImageField.html')

    def __call__(self, **kwargs):
        return self.widget(**kwargs)     
        


def create_view(self, cls, *args, **kwargs):
    self._template_args['form'] = self.create_form()
    if self.inline_models:
        self._template_args['form_opts'] = FormOpts(widget_args=getattr(self, 'form_widget_args', {}))

    create_template = self.create_template
    if cls.template_mode != 'genshi':
        create_template = cls.scaffold_form()

    kwargs['form'] = self._template_args['form']
    return self.render(create_template, **kwargs)

class MyModelView(ModelView):
    def create_view(self, **kwargs):
        # Ваша логика
        return super(MyModelView, self).create_view(**kwargs)



       

class Car(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(100))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    drive = db.Column(db.String(50))
    car_class = db.Column(db.String(50))
    fuel_type = db.Column(db.String(50))
    country = db.Column(db.String(50))
    transmission = db.Column(db.String(50))
    color = db.Column(db.String(50))
    seats = db.Column(db.Integer)
    state_number = db.Column(db.String(50))
    engine_volume = db.Column(db.Float)
    horsepower = db.Column(db.Integer)
    gearbox_type = db.Column(db.String(50))
    max_speed = db.Column(db.Integer)
    fuel_consumption = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    fuel_brand = db.Column(db.String(50))
    fuel_tank_volume = db.Column(db.Integer)
    trunk_volume = db.Column(db.Integer)
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    interior = db.Column(db.String(100))
    has_air_conditioning = db.Column(db.Boolean)
    has_tinting = db.Column(db.Boolean)
    color_description = db.Column(db.String(100))
    vin = db.Column(db.String(50))
    registration_certificate = db.Column(db.String(100))
    short_description = db.Column(db.Text)
    detailed_description = db.Column(db.Text)
    primary_image = db.Column(db.String(100))
    # Добавление связи с изображениями
    images = db.relationship('CarImage', backref='car', lazy=True)
    # Цены
    price_1_day = db.Column(db.Float)
    price_2_5_days = db.Column(db.Float)
    price_6_15_days = db.Column(db.Float)
    price_16_29_days = db.Column(db.Float)
    price_30_days = db.Column(db.Float)
    with_driver = db.Column(db.Boolean)
    driver_price_3_hours = db.Column(db.Float)
    driver_price_3_6_hours = db.Column(db.Float)
    driver_price_7_12_hours = db.Column(db.Float)
    driver_price_13_hours = db.Column(db.Float)
    purchase_price = db.Column(db.Float)
    deposit = db.Column(db.Float)
    meta_title = db.Column(db.String(100))
    meta_keywords = db.Column(db.String(100))
    meta_description = db.Column(db.String(100))
    is_hidden = db.Column(db.Boolean)
    is_not_counted = db.Column(db.Boolean)
    is_not_rented = db.Column(db.Boolean)
    is_in_repair = db.Column(db.Boolean)
    no_contract_print = db.Column(db.Boolean)
    is_not_shown_to_customers = db.Column(db.Boolean)
    always_occupied = db.Column(db.Boolean)
    occupied_until = db.Column(db.DateTime)
    occupied_days_ahead = db.Column(db.Integer)
    additional_cities = db.Column(db.Text)  # Список дополнительных городов в виде строки или JSON

    

class ImageForm(FlaskForm):
    image = FileField(validators=[
        FileAllowed(['jpg', 'png'], 'Только изображения!')
    ])
class CarImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    image_url = db.Column(db.String(100))
                            
class CarView(ModelView):
    form_columns = ['name', 'url', 'brand', 'model', 'drive', 'car_class', 'fuel_type', 'country', 'transmission', 'color', 'seats', 'state_number',
        'engine_volume', 'horsepower', 'gearbox_type', 'max_speed', 'fuel_consumption', 'dimensions', 'fuel_brand', 'fuel_tank_volume', 'trunk_volume', 'year', 'mileage',
        'interior', 'has_air_conditioning', 'has_tinting', 'color_description', 'vin', 'registration_certificate', 'short_description', 'detailed_description', 'primary_image', 'images', 'price_1_day',
        'price_2_5_days', 'price_6_15_days', 'price_16_29_days', 'price_30_days', 'with_driver', 'driver_price_3_hours', 'driver_price_3_6_hours', 'driver_price_7_12_hours',
        'driver_price_13_hours', 'purchase_price', 'deposit', 'meta_title', 'meta_keywords', 'meta_description', 
        'is_hidden', 'is_not_counted', 'is_not_rented', 'is_in_repair', 'no_contract_print',  
        'is_not_shown_to_customers', 'always_occupied', 'occupied_until',  'occupied_days_ahead', 'additional_cities' ]
    form_extra_fields = {
        'primary_image': ImageUploadField('Основное изображение',
                                          base_path='/path/to/images/',
                                          url_relative_path='/images/'),
        'images': MultiImageField(label='Дополнительные изображения')
    }
    form_overrides = {
    'images': MultiImageField() # экземпляр класса без cls
}
    
def on_model_change(self, form, model, is_created):
    try:
        # Обработка основного изображения
        if form.primary_image.data:
            file_data = form.primary_image.data
            # Генерация уникального имени файла
            filename = f"{model.id}-{model.brand}-{model.model}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{os.path.splitext(file_data.filename)[1]}"
            file_path = os.path.join(self.get_save_path(), filename)
            file_data.save(file_path)
            model.primary_image = filename  # Сохраняем только имя файла в модели

        # Обработка дополнительных изображений
        if form.additional_images.data:
            for image_form in form.additional_images.entries:
                image_data = image_form.image.data
                if image_data:
                    # Генерация уникального имени файла
                    filename = f"{model.id}-{model.brand}-{model.model}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{os.path.splitext(image_data.filename)[1]}"
                    file_path = os.path.join(self.get_save_path(), 'additional', filename)
                    image_data.save(file_path)
                    # Создаем объекты CarImage и добавляем их в сессию базы данных
                    new_image = CarImage(car=model, image_url=filename)  # Сохраняем только имя файла
                    db.session.add(new_image)
            db.session.commit() 

    except Exception as e:
        logger.error(f'Ошибка при обработке изображений: {e}')
        db.session.rollback()
        raise e  
            
class CarForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    url = StringField('URL')
    primary_image = FileField('Основное изображение', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png'], 'Только изображения!')
    ])
    additional_images = FileField(FormField(ImageForm), min_entries=1)
    submit = SubmitField('Добавить авто')

class StatusEnum(enum.Enum):
    new = 'Новый'
    in_progress = 'В обработке'
    completed = 'Завершен'
    cancelled = 'Отменен'

## конец настройки авто

  
# Добавление представления модели User в админ-панель
admin.add_view(UserView(User, db.session))
admin.add_view(CarView(Car, db.session, name='Автомобили'))




# Настройка логгера
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
@app.before_request
def before_request():
    language = request.cookies.get('language', 'ru')  # По умолчанию русский

    # Если язык не поддерживается, установите значение по умолчанию
    if language not in ['ru', 'en', 'es']:
        language = 'ru'

    # Если язык не задан в cookie, установите его на основе предпочтений браузера
    if not language:
        language = request.accept_languages.best_match(['ru', 'en', 'es'])
        response = make_response(redirect(request.url))
        response.set_cookie('language', language)
        return response      

@app.route('/page/<slug>')
def show_page(slug):
    app.logger.debug(f'Request for page with slug: {slug}')
    try:
        page = Page.query.filter_by(slug=slug).first_or_404()
        return render_template('page.html', page=page)
    except Exception as e:
        app.logger.error(f'Error loading page with slug {slug}: {e}')
        raise e  # Это вызовет стандартную страницу ошибки Flask


    
@app.route('/catalog')
def catalog():
    return render_template('catalog.html', name="catalog")
    
@app.route('/news')
def show_news():
    news_items = News.query.order_by(News.created_at.desc()).all()
    return render_template('news.html', news=news_items)
    
   
          
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Маршруты Flask

    
@app.route('/')
def index():

    # Получение списка автомобилей (если это необходимо)
    cars = Car.query.all()

    return render_template('main.html', cities=cities, cars=cars, name="main")  
         

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        # ... создание и сохранение нового автомобиля в базе данных
        flash('Автомобиль успешно добавлен')
        return redirect(url_for('index'))
    return render_template('add_car.html', form=form)    

     
    
@app.route('/filter', methods=['GET'])
def filter_results():
    start_booking = request.args.get('start_booking')
    end_booking = request.args.get('end_booking')
    price_range = request.args.get('price_range')
    akpp = request.args.get('akpp') == 'on'
    autostart = request.args.get('autostart') == 'on'
    air_conditioner = request.args.get('air_conditioner') == 'on'
    navigator = request.args.get('navigator') == 'on'
    seats_count = request.args.get('seats_count')
    
    # Здесь должен быть запрос к базе данных с использованием полученных параметров
    cars = Car.query.filter(Car.start_booking >= start_booking, 
                            Car.end_booking <= end_booking,
                            Car.price <= price_range,
                            Car.akpp == akpp,
                            Car.autostart == autostart,
                            Car.air_conditioner == air_conditioner,
                            Car.navigator == navigator,
                            Car.seats_count >= seats_count).all()
    return render_template('cars.html', cars=cars)    



@app.route('/admin/orders')
@login_required
def admin_orders():
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)

       

# Настройка доступных языков и стандартного языка
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Moscow'
app.config['LANGUAGES'] = {
    'en': 'English',
    'es': 'Español',
    'ru': 'Русский'
}      
            
    
# Запуск Flask-приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083, debug=True)

