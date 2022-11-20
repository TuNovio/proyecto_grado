from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)
from myblog import db
from myblog.models.paciente import Paciente
from werkzeug.exceptions import abort
import pyperclip


pacientes = Blueprint('pacientes', __name__)
# productos =Blueprint('productos', __name__, url_prefix='/productos')
# add string to the end on loop


def busqueda_paciente(requestform):
    #TODO : FIX
    pacientes = Paciente.query.all()
    pacientes=pacientes
    pacientes=pacientes[:5]
    # paciente = db.session.query(Paciente).order_by(Paciente.cedula).filter(
    #     Paciente.cedula.like("%"+requestform+"%")).all()
    return pacientes


@pacientes.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST' and "txtcategoria" in request.form:
        if (request.form['txtcategoria'] == '' or request.form['txtcategoria'] == " "):
            requestform = None
            pacientes = Paciente.query.all()
            pacientes=pacientes
            pacientes=pacientes[:5]
            db.session.commit()
            return render_template('paciente/index.html', pacientes=pacientes)
        else:
            requestform=request.form['txtcategoria']
            pacientes=busqueda_paciente(requestform)
            return render_template('paciente/index.html', pacientes=pacientes)
    else:
        requestform=None
        pacientes=busqueda_paciente(requestform)
    return render_template('paciente/index.html', pacientes=pacientes)


@pacientes.before_request
def g_producto():
    g_producto=session.get('g_producto')
    if g_producto is None:
        g.productoGlobal=None
    else:
        g.productoGlobal=g_producto
# cedula# tipo_documento# nombre# edad# genero# tipo_subsidio# fecha_nacimiento
@pacientes.route('/register', methods=('GET', 'POST'))
def register():    
    if request.method == 'POST':
        cedula = request.form['cedula']
        tipo_documento = request.form['tipo_documento']
        nombre = request.form['nombre']
        edad = request.form['edad']
        genero = request.form['genero']
        tipo_subsidio = request.form['tipo_subsidio']
        fecha_nacimiento = request.form['fecha_nacimiento']
        paciente = Paciente(cedula, tipo_documento, nombre, edad, genero, tipo_subsidio, fecha_nacimiento)
        error = None
        if not cedula:
            error = 'Cedula es requerida.'
        elif not tipo_documento:
            error = 'Tipo de documento es requerido.'
        elif not nombre:
            error = 'Nombre es requerido.'
        elif not edad:
            error = 'Edad es requerida.'
        elif not genero:
            error = 'Genero es requerido.'
        elif not tipo_subsidio:
            error = 'Tipo de subsidio es requerido.'
        elif not fecha_nacimiento:
            error = 'Fecha de nacimiento es requerida.'  
        print("paciente:", paciente)
        # user_name=User.query.filter_by(username=username).first()
        cedExist = Paciente.query.get(cedula)        
        if error is None and cedExist == None:
            db.session.add(paciente)
            db.session.commit()
            error = f'Paciente {nombre} : {cedula} DONE'
            return redirect(url_for('paciente.index'))
        else:
            error = f'ERROR: la cedula {cedula}, ya esta registrado'
        flash(error)
        # return redirect(url_for('auth.login'))
    return render_template('paciente/register.html')
def get_paciente(cedula):
    # producto = Producto.query.filter_by(id=id).first()
    paciente = Paciente.query.get(cedula)
    if paciente is None:
        abort(404, "Producto id {0} doesn't exist.".format(id))
    return paciente

@pacientes.route('/paciente/delete/<int:cedula>', methods=('GET', 'POST'))
def delete(cedula):
    paciente = get_paciente(cedula)
    db.session.delete(paciente)
    db.session.commit()
    return redirect(url_for('pacientes.index'))

@pacientes.route('/update/<int:cedula>', methods=('GET', 'POST'))
def update(cedula):
    miPaciente = get_paciente(cedula)
    error = None
    if request.method == 'POST':       
        if (miPaciente != None and miPaciente.cedula != miPaciente.cedula):
            error = f'ERROR: el codprod {miPaciente.cedula}, ya esta registrado'
            flash(error)
            return render_template('paciente/update.html', paciente=miPaciente)
        miPaciente.tipo_documento = request.form.get('tipo_documento')
        miPaciente.cedula = request.form.get('cedula')
        miPaciente.nombre = request.form.get('nombre')
        miPaciente.edad = request.form.get('edad')
        miPaciente.genero = request.form.get('genero')
        miPaciente.tipo_subsidio = request.form.get('tipo_subsidio')
        miPaciente.fecha_nacimiento = request.form.get('fecha_nacimiento')
        if not miPaciente.tipo_documento:
            error = 'Se requiere tipo_documento'
        elif not miPaciente.cedula:
            error = 'Se requiere cedula'
        elif not miPaciente.nombre:
            error = 'Se requiere nombre'
        elif not miPaciente.edad:
            error = 'Se requiere edad'
        elif not miPaciente.genero:
            error = 'Se requiere genero'
        elif not miPaciente.tipo_subsidio:
            error = 'Se requiere tipo_subsidio'
        elif not miPaciente.fecha_nacimiento:
            error = 'Se requiere fecha_nacimiento'
        else:
            db.session.add(miPaciente)
            db.session.commit()
            return redirect(url_for('pacientes.index'))
        flash(error)
    return render_template('paciente/update.html', paciente=miPaciente)
