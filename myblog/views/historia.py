from datetime import date
from flask import (
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)
from sqlalchemy import func

from myblog import db

from myblog.models.compra import Compra
from myblog.models.detcompra import DetCompra
from myblog.models.producto import Producto
from myblog.models.tercero import Tercero
from myblog.views.auth import login_required
from werkzeug.exceptions import abort

from myblog.views.productos import busqueda_producto_cache

compras = Blueprint('compras', __name__, url_prefix='/compras')

def update_compra(id_compra):
    detCompras = DetCompra.query.filter(DetCompra.numcom==id_compra).all()
    compra     = Compra.query.get(id_compra)  
    print("*"*100)
    print(detCompras)
    print("*"*100)
    compra.subcom = 0
    compra.totiva = 0
    compra.totcom = 0
    for detCompra in detCompras:
        compra.subcom = compra.subcom + (detCompra.valuni*detCompra.candet) #909.09 or 1000
        compra.totiva = compra.totiva + (detCompra.ivapes*detCompra.candet) #90.91 or 100
        compra.totcom = compra.totcom + (detCompra.valuni*detCompra.candet) + (detCompra.ivapes*detCompra.candet)#1000 or 1100
        db.session.add(compra)
    db.session.commit()
@compras.route("/", methods=('GET', 'POST'))
@login_required
def index():
    # TODO tercero default
    if request.method == 'POST' and "txtcategoria" in request.form:
        if (request.form['txtcategoria'] == ''):
            compras = reversed(Compra.query.all())
            compras = list(compras)
            compras = compras[:5]
            db.session.commit()
        else:
            print("**"*20)
            compras1 = db.session.query(Compra).filter(
                Compra.numcom.like("%"+request.form['txtcategoria']+"%")).all()
            compras2 = db.session.query(Compra).order_by(Compra.docext).filter(
                Compra.docext.like("%"+request.form['txtcategoria']+"%")).all()
            compras = compras1 + compras2
            db.session.commit()
            return render_template('compra/index.html', compras=compras)
    else:
        compras = reversed(Compra.query.all())
        compras = list(compras)
        compras = compras[:5]
        db.session.commit()
    return render_template('compra/index.html', compras=compras)


@compras.route('/registerTercero', methods=('GET', 'POST'))
@login_required
def registerTercero():
    print("*"*50)
    print("baseurl", request.base_url)
    print("path", request.path)
    print("fullpath", request.full_path)
    print("scriptroot", request.script_root)
    print("url", request.url)
    terceros = reversed(Tercero.query.all())
    terceros = list(terceros)
    terceros = terceros[:5]
    if request.method == 'POST' and "txtcategoria" in request.form:
        if (request.form['txtcategoria'] == ''):
            db.session.commit()
        else:
            terceros1 = db.session.query(Tercero).filter(
                Tercero.nitter.like("%"+request.form['txtcategoria']+"%")).all()
            terceros2 = db.session.query(Tercero).order_by(Tercero.nomcom).filter(
                Tercero.nomcom.like("%"+request.form['txtcategoria']+"%")).all()
            terceros = terceros1 + terceros2
            db.session.commit()
            return render_template('compra/registerTercero.html', terceros=terceros)
    return render_template('compra/registerTercero.html', terceros=terceros)


@compras.route('/registerCompra/<string:id>', methods=('GET', 'POST'))
@login_required
def registerCompra(id):
    tercero = Tercero.query.get(id)
    print("*"*50)
    print("baseurl", request.base_url)
    print("path", request.path)
    print("fullpath", request.full_path)
    print("scriptroot", request.script_root)
    print("url", request.url)
    # last_compra = Compra.query.order_by(Compra.numcom.desc()).first()
    last_compra = reversed(Compra.query.all())
    last_compra = list(last_compra)
    last_compra = last_compra[:1]
    last_compra = int(last_compra[0].numcom) + 1
    error = None
    if request.method == 'POST':
        numcom = request.form['numcom']
        docext = request.form['docext']
        feccom = request.form['feccom']
        vencom = request.form['vencom']
        horcom = request.form['horcom']
        forpag = request.form['forpag']
        nitter = tercero.nitter
        nomter = tercero.nomcom
        dirter = tercero.dirter
        telter = tercero.telter
        corele = tercero.corele
        codemp = g.user.username
        nomdoc = "COMPRA"
        subcom = 0
        totiva = 0
        totcom = 0
        estcom = "B"
        obscom = ""
        codclas = "S18"
        totdct = 0
        totaju = 0
        compra = Compra(numcom, nomdoc, docext, feccom, vencom, nitter, nomter, dirter, telter, corele,
                        subcom, totiva, totcom, estcom, codemp, horcom, obscom, codclas, forpag, totdct, totaju)
        if not numcom:
            error = 'numcom is required.'
        # elif not nomdoc:
        #     error = 'nomdoc is required.'
        elif not docext:
            error = 'docext is required.'
        elif not feccom:
            error = 'feccom is required.'
        elif not vencom:
            error = 'vencom is required.'
        elif not codemp:
            error = 'codemp is required.'
        elif not horcom:
            error = 'horcom is required.'
        if error is not None:
            error = 'Error al registrar la compra ' + error
        else:
            db.session.add(compra)
            db.session.commit()
            # TODO mostrar error
            error = f'Compra {numcom} : {nitter} DONE'
            print("*"*10, error)
            return redirect(url_for('compras.registerProductos', id=numcom))
            # return render_template('compra/registerCompra.html',compra=compra.numcom)
        flash(error)
    return render_template('compra/registerCompra.html', last_compra=last_compra)


@compras.route('/registerProductos/<string:id>', methods=('GET', 'POST'))
def registerProductos(id):
    update_compra(id)
    compra=Compra.query.get(id)
    productos_Compra = DetCompra.query.filter(DetCompra.numcom ==id).all() 
    if request.method == 'POST' and "txtcategoria" in request.form:
        if (request.form['txtcategoria'] == '' or request.form['txtcategoria'] == " "):
            requestform = None
            productos = busqueda_producto_cache(requestform)
            return render_template('compra/registerProductos.html', productos=productos, id_compra=id, productos_Compra=productos_Compra, compra=compra)
        else:            
            requestform = request.form['txtcategoria']
            productos = busqueda_producto_cache(requestform)
            return render_template('compra/registerProductos.html', productos=productos, id_compra=id, productos_Compra=productos_Compra, compra=compra)
    else:
        requestform = None
        productos = busqueda_producto_cache(requestform)
    return render_template('compra/registerProductos.html', productos=productos, id_compra=id, productos_Compra=productos_Compra, compra=compra)

@compras.before_request
def g_producto():
    g_producto = session.get('g_producto')
    if g_producto is None:
        g.productoGlobal = None
    else:
        g.productoGlobal = g_producto

def valorFloat(num):
    try:
        num = float("%.2f" % float(num))
    except ValueError:
        num = num
    return num

#TODO ALIMINAR PRODUCTO SI YA EXISTE
@compras.route('/registerProductos/<string:id_compra>/Agregar/<int:id_producto>', methods=('GET', 'POST'))
@login_required
def agregarProducto(id_compra, id_producto):
    compra = Compra.query.get(id_compra)
    producto = Producto.query.get(id_producto)
    # producto_Compra_Repetido = DetCompra.query.filter(DetCompra.numcom == id_compra , DetCompra.codprod == id_producto).first()
    # max_numcom = db.session.query(func.max(DetCompra.numcom == id_compra)).scalar()
    # query = db.session.query(DetCompra.numcom).filter(DetCompra.numcom == id_compra).all()
    max_numite = db.session.query(func.max(DetCompra.numite)).filter(DetCompra.numcom == id_compra).scalar()
    # for i in query:
    #     #get max numite
    #     max_numite = db.session.query(func.max(DetCompra.numite)).filter(DetCompra.numcom == i[0]).scalar()    
    print("#"*10,"\n", max_numite, "\n", "#"*10)    
    query=max_numite
    if request.method == 'POST':
        # TODO IDEA evitar errores de duplicidad de productos
        numcom = compra.numcom  
        codprod = producto.codprod  
        nomdet = producto.nomprod  
        venfec = date.today() #str
        ivapor = float(request.form['ivapor'])        
        valor = valorFloat(request.form['valuni'])        
        dctpor = float(request.form['dctpor'])
        candet = int(request.form['candet'])
        if(request.form['ivaIncluido'] == '1'):
            valuni = valorFloat(valor/((ivapor/100)+1)) # 1000/1.1 = 909.09 
            ivapes = valorFloat((valor-valuni) )# 1000 - 909.09 = 90.91    
            ivapes = valorFloat(ivapes-(ivapes*dctpor/100) )# 90.91 - (90.91*10/100) = 81.82
            cosuni = valorFloat(valor )# 1000
            cosuni = valorFloat(cosuni-(cosuni*dctpor/100) )# 1000 - (1000*10/100) = 900
            totdet = valorFloat(cosuni*candet)
        else:
            valuni = valorFloat( valor )# 1000
            cosuni = valorFloat(valor*((ivapor/100)+1))# 1000*1.1 = 1100
            ivapes = valorFloat(cosuni-valor )#1100-1000= 100      
            totdet = valorFloat(cosuni*candet)
        if(query == None):
            numite = 1
        else:
            numite = str(query+1) 
        codclas = request.form['codclas']
        undfra = producto.undfra 
        detcompra = DetCompra(numcom, codprod, nomdet, venfec, valuni, candet,
                              ivapor, ivapes, cosuni, totdet, numite, codclas, dctpor, undfra)        
        print("*"*50, "\n", valuni,  ivapes, cosuni, totdet,  "\n", "*"*50)
        # compra.subcom = compra.subcom + (cosuni*candet)
        # compra.totiva = compra.totiva + (ivapes*candet)
        # compra.totcom = compra.totcom + (valuni *candet + ivapes*candet)
        producto_Compra_Repetido= None
        producto_Compra_Repetido = DetCompra.query.filter(DetCompra.numcom == id_compra , DetCompra.codprod == id_producto).first()
        #TODO ERRORES ELIF
        if producto_Compra_Repetido is not None:        
            db.session.delete(producto_Compra_Repetido)
            # compra= Compra.query.get(id_compra)
            # compra.subcom = compra.subcom - (cosuni*candet)
            # compra.totiva = compra.totiva - (ivapes*candet)
            # compra.totcom = compra.totcom - (ivapes*candet) - (valuni*candet)
            # db.session.add(compra)
        producto.exiprod = producto.exiprod + candet
        producto.cosulc = cosuni        
        db.session.add(detcompra)
        db.session.add(producto)
        # update_compra(id_compra)
        db.session.commit()
        return redirect(url_for('compras.registerProductos', id=id_compra))
    return render_template('compra/agregarProducto.html', compra=compra, producto=producto)

def find_producto_DetCompra( id_compra, id_producto):
    productos_Compra = DetCompra.query.filter(DetCompra.numcom ==id_compra and DetCompra.codpro ==id_producto).first()
    if productos_Compra is None:
        abort(404, f"Producto id_compra: {id_compra}, id_producto: {id_producto}, doesn't exist.")    
    return productos_Compra

@compras.route('/delete/<id_compra>/<id_producto>', methods=('GET', 'POST'))
@login_required
def delete( id_compra, id_producto):    
    producto_Compra = DetCompra.query.filter(DetCompra.numcom ==id_compra   ,  DetCompra.codprod ==id_producto).first()
    # compra= Compra.query.get(id_compra)
    # compra.subcom = compra.subcom - (producto_Compra.cosuni*producto_Compra.candet)
    # compra.totiva = compra.totiva - (producto_Compra.ivapes*producto_Compra.candet)
    # compra.totcom = compra.totcom - (producto_Compra.ivapes*producto_Compra.candet) - (producto_Compra.valuni*producto_Compra.candet)
    #----------------------------------------------------------------------AND-------------------------------------------
    # producto_Compra = DetCompra.query.filter(DetCompra.numcom ==id_compra and DetCompra.codprod ==id_producto).first()    
    producto = Producto.query.get(producto_Compra.codprod)
    producto.exiprod = producto.exiprod - producto_Compra.candet
    db.session.add(producto)
    db.session.delete(producto_Compra)    
    db.session.commit()
    return redirect(url_for('compras.registerProductos',id=id_compra))

@compras.route('/anular/<id_compra>', methods=('GET', 'POST'))
def anular( id_compra ):
    detCompra = DetCompra.query.filter(DetCompra.numcom ==id_compra).all() 
    print("*"*50,"\n", detCompra, "\n", "*"*50)
    error=None
    for producto_Compra in detCompra:
        find_producto_DetCompra(id_compra, producto_Compra.codprod)
        producto = Producto.query.get(producto_Compra.codprod)
        producto.exiprod = producto.exiprod - producto_Compra.candet
        db.session.add(producto)
        db.session.delete(producto_Compra)
        db.session.commit()

    
    compra= Compra.query.get(id_compra)
    if(compra is not None):
        db.session.delete(compra)   
        db.session.commit()
        print("*"*50,"\n", compra, "\n", "*"*50)


    else:
        error = "No se pudo encontro la compra a anular "
    if(error is None):
        flash(f'Compra {id_compra} anulada correctamente')
        return redirect(url_for('compras.index'))

        
    return redirect(url_for('compras.registerProductos',id=id_compra))