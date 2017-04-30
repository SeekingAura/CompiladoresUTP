# coding: utf-8
'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
árbol de sintaxis abstracto.  Durante el análisis sintático, se debe
crear estos nodos y conectarlos.  En general, usted tendrá diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deberá
añadir más.
'''

# NO MODIFICAR

class AST(object):
	'''
	Clase base para todos los nodos del AST.  Cada nodo se espera
	definir el atributo _fields el cual enumera los nombres de los
	atributos almacenados.  El método a continuación __init__() toma
	argumentos posicionales y los asigna a los campos apropiados.
	Cualquier argumento adicional especificado como keywords son
	también asignados.
	'''
	_fields = []
	def __init__(self, *args, **kwargs):
		self.tipo=None
		assert len(args) == len(self._fields)
		for name,value in zip(self._fields,args):
			setattr(self,name,value)

		# Asigna argumentos adicionales (keywords) si se suministran
		for name,value in kwargs.items():
			setattr(self,name,value)
	
	def __repr__(self):
		return self.__class__.__name__
		
	def pprint(self):
		for depth, node in flatten(self):
			print("%s%s" % (" "*(4*depth),node))
			
	
			
def validate_fields(**fields):
	def validator(cls):
		old_init = cls.__init__
		def __init__(self, *args, **kwargs):
			old_init(self, *args, **kwargs)
			for field,expected_type in fields.items():
				assert isinstance(getattr(self, field), expected_type)
		cls.__init__ = __init__
		return cls
	return validator
	
# ----------------------------------------------------------------------
# Nodos AST especificos
#
# Para cada nodo es necesario definir una clase y añadir la 
# especificación del apropiado _fields = [] que indique que campos
# deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresión izquierda y derecha, como esto:
#
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Unos pocos nodos ejemplos

@validate_fields(modulos = list)
class Lola(AST):
	_fields=['modulos']
	def append(self, modu):
		self.modulos.append(modu)

class TipoSimpleBasico(AST):
	_fields = ['tipoBasico']
	#def append(self, temp):

class TipoSimpleID(AST):
	_fields = ['ID']
	
class TipoSimpleIDListaExpresion(AST):
	_fields = ['ID', 'ListaExpresiones']

class TipoBasico(AST):#valor constante
	_fields = ['tipoBasico']
	
@validate_fields(expresionesLista = list)
class ListaExpresiones(AST):
	_fields = ['expresionesLista']
	def append(self, expr):
		self.expresionesLista.append(expr)

class Tipo(AST):
	_fields = ['tipoExpresiones', 'tipoSimple']
	
class TipoExpresiones(AST):
	_fields = ['tipoExpresionesR']

@validate_fields(expresionesTipo = list)
class TipoExpresionesR(AST):
	_fields = ['expresionesTipo']
	def append(self, expr):
		self.expresionesTipo.append(expr)

class DeclaracionConstante(AST):
	_fields = ['ID', 'expresion']
		
class DeclaracionVariable(AST):
	_fields = ['listaId', 'tipos']

@validate_fields(idsListaId = list)
class ListaId(AST):
	_fields = ['idsListaId']
	def append(self, Id):
		self.idsListaId.append(Id)
		
class Selector(AST):
	_fields = ['selectorR']
	
@validate_fields(selectorRRs = list)
class SelectorR(AST):
	_fields = ['selectorRRs']
	def append(self, selector):
		self.selectorRRs.append(selector)
		
class SelectorRR(AST):
	_fields = ['ID', 'INTEGER', 'expresion']

class FactorSelector(AST):
	_fields = ['ID', 'selector']

class FactorValor(AST):
	_fields = ['value']
	
	
class FactorSimbolo(AST):
	_fields = ['simbolo', 'factor']
	
@validate_fields(expresionesFactor = list)
class FactorDeclaracion(AST):
	_fields=['declaracion', 'expresionesFactor']

@validate_fields(simbolosTermino = list, factoresTermino = list)
class Termino(AST):
	_fields = ['simbolosTermino', 'factoresTermino']
	def append(self, simboloTermino, factor):
		self.simbolosTermino.append(simboloTermino)
		self.factoresTermino.append(factor)

@validate_fields(simbolosExpresion = list, terminosExpresion = list)
class Expresion(AST):
	_fields=['simbolosExpresion', 'terminosExpresion']
	def append(self, simboloExpresion, terminoExpresion):
		self.simbolosExpresion.append(simboloExpresion)
		self.terminosExpresion.append(terminoExpresion)
	
class Asignacion(AST):
	_fields = ['ID', 'selector', 'expresion']
	
class AsignacionCondicion(AST):
	_fields = ['ID', 'selector', 'condicion', 'expresion']

class Condicion(AST):
	_fields = ['expresion']
	
class Relacion(AST):
	_fields = ['expresion0', 'simbolo', 'expresion1']
	
class SentenciaSi(AST):
	_fields = ['relacion', 'sentenciaSecuencia', 'sentenciaSiSino', 'sentenciaSiEntonces']

class SentenciaSiSino(AST):
	_fields = ['sentenciaSiSinoR']

@validate_fields(relacionesSentenciaSiSinoR = list, sentenciasSecuenciaSentenciaSiSinoR = list)
class SentenciaSiSinoR(AST):#elsif
	_fields = ['relacionesSentenciaSiSinoR', 'sentenciasSecuenciaSentenciaSiSinoR']
	def append(self, relacion, sentenciaSecuencia):
		self.relacionesSentenciaSiSinoR.append(relacion)
		self.sentenciasSecuenciaSentenciaSiSinoR.append(sentenciaSecuencia)

class SentenciaSiEntonces(AST):
	_fields = ['sentenciaSecuencia']
	
class SentenciaPara(AST):
	_fields = ['ID', 'expresionDesde', 'expresionHasta', 'sentenciaSecuencia']

class Sentencia(AST):
	_fields = ['sentencia']

@validate_fields(sentenciasSecuencia = list)
class SentenciaSecuencia(AST):
	_fields = ['sentenciasSecuencia']
	def append(self, sentencia):
		self.sentenciasSecuencia.append(sentencia)
	
class Modulo(AST):
	_fields = ['ID0', 'declaracionTipoPuntoComa', 'declaracionConstanteCONST', 'declaracionVariableIN', 'declaracionVariableINOUT', 'declaracionVariableOUT', 'declaracionVariableVAR', 'declaracionRelacionPOS', 'sentenciaSecuenciaBEGIN', 'ID1']
	
class DeclaracionTipoPuntoComa(AST):
	_fields = ['declaracionTipoPuntoComaR'] 

@validate_fields(declaracionesTipo = list)
class DeclaracionTipoPuntoComaR(AST):
	_fields = ['declaracionesTipo']
	def append(self, declaracionTipo):
		self.declaracionesTipo.append(declaracionTipo)

class DeclaracionConstanteCONST(AST):
	_fields = ['declaracionConstanteRecursivo']
	
class DeclaracionConstanteRecursivo(AST):
	_fields = ['declaracionConstanteRecursivoR']
	
@validate_fields(declaracionesConstante = list)
class DeclaracionConstanteRecursivoR(AST):
	_fields = ['declaracionesConstante']

	def append(self, declaracionConstante):
		self.declaracionesConstante.append(declaracionConstante)
		
class DeclaracionVariableIN(AST):
	_fields = ['declaracionVariableRecursivo']
		
class DeclaracionVariableRecursivo(AST):
	_fields = ['declaracionVariableRecursivoR']
		
@validate_fields(declaracionesVariable = list)
class DeclaracionVariableRecursivoR(AST):
	_fields = ['declaracionesVariable']
	def append(self, declaraVariable):
		self.declaracionesVariable.append(declaraVariable)

class DeclaracionVariableINOUT(AST):
	_fields = ['declaracionVariableRecursivo']
	
class DeclaracionVariableOUT(AST):
	_fields = ['declaracionVariableRecursivo']
	
class DeclaracionVariableVAR(AST):
	_fields = ['declaracionVariableRecursivo']
	
class DeclaracionRelacionPOS(AST):
	_fields = ['declaracionRelacionRecursivo']

class DeclaracionRelacionRecursivo(AST):
	_fields = ['declaracionRelacionR']

@validate_fields(relaciones = list)
class DeclaracionRelacionR(AST):
	_fields = ['relaciones']
	def append(self, relacion):
		self.relaciones.append(relacion)
	
class SentenciaSecuenciaBEGIN(AST):
	_fields = ['sentenciaSecuencia']
	
class TipoFormal(AST):
	_fields = ['expresionCorcheteO']

class ExpresionCorcheteO(AST):
	_fields = ['expresionCorcheteOR']
	
@validate_fields(expresionesOpcional = list)
class ExpresionCorcheteOR(AST):
	_fields = ['expresionesOpcional']
	def append(self, expresionOpcional):
		self.expresionesOpcional.append(expresionOpcional)

class ExpresionOpcional(AST):
	_fields = ['expresion']
	
class TipoFormalBus(AST):
	_fields = ['expresionCorcheteO', 'tipoBus']

class DeclaracionTipo(AST):
	_fields = ['ID0', 'simboloPor', 'listaIdParentesis', 'declaracionConstanteCONST', 'tipoFormalIN', 'tipoFormalINOUT', 'declaracionVariableOUT', 'declaracionVariableVAR', 'declaracionRelacionPOS', 'sentenciaSecuenciaBEGIN', 'ID1']
	
class ListaIdParentesis(AST):
	_fields = ['listaId']
	
class TipoFormalIN(AST):
	_fields = ['tipoFormallistaId']
	
class TipoFormallistaId(AST):
	_fields = ['tipoFormallistaIdR']
	
@validate_fields(listasId = list, tiposFormal = list)
class TipoFormallistaIdR(AST):
	_fields = ['listasId', 'tiposFormal']
	def append(self, listaId, tipoFormal):
		self.listasId.append(listaId)
		self.tiposFormal.append(tipoFormal)

class TipoFormalINOUT(AST):
	_fields = ['tipoFormlBuslistaId']
		
class TipoFormlBuslistaId(AST):
	_fields = ['tipoFormlBuslistaIdR']
		
@validate_fields(listasId = list, tiposFormalBus = list)
class TipoFormlBuslistaIdR(AST):
	_fields = ['listasId', 'tiposFormalBus']
	def append(self, listaId, tipoFormalBus):
		self.listasId.append(listaId)
		self.tiposFormalBus.append(tipoFormalBus)
		
class AsignacionUnidad(AST):
	_fields = ['ID', 'selector', 'listaExpresiones']
		


	
# Usted deberá añadir mas nodos aquí.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration,
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
	'''
	Clase para visitar nodos del árbol de sintaxis.  Se modelá a partir
	de una clase similar en la librería estándar ast.NodeVisitor.  Para
	cada nodo, el método visit(node) llama un método visit_NodeName(node)
	el cual debe ser implementado en la subclase.  El método genérico
	generic_visit() es llamado para todos los nodos donde no hay 
	coincidencia con el método visit_NodeName().
	
	Es es un ejemplo de un visitante que examina operadores binarios:
	
	class VisitOps(NodeVisitor):
		visit_Binop(self,node):
			print("Operador binario", node.op)
			self.visit(node.left)
			self.visit(node.right)
		visit_Unaryop(self,node):
			print("Operador unario", node.op)
			self.visit(node.expr)
	
	tree = parse(txt)
	VisitOps().visit(tree)
	'''
	def visit(self,node):
		'''
		Ejecuta un método de la forma visit_NodeName(node) donde
		NodeName es el nombre de la clase de un nodo particular.
		'''
		if node:
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			return visitor(node)
		else:
			return None
			
	def generic_visit(self,node):
		'''
		Método ejecutado si no se encuentra médodo aplicable visit_.
		Este examina el nodo para ver si tiene _fields, es una lista,
		o puede ser recorrido completamente.
		'''
		#
		#print("entro")
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, AST):
						self.visit(item)
			elif isinstance(value, AST):
				self.visit(value)
		
# NO MODIFICAR
class NodeTransformer(NodeVisitor):
	'''
	Clase que permite que los nodos del arbol de sintaxis sean
	reemplazados/reescritos.  Esto es determinado por el valor retornado
	de varias funciones visit_().  Si el valor retornado es None, un
	nodo es borrado. Si se retorna otro valor, reemplaza el nodo
	original.
	
	El uso principal de esta clase es en el código que deseamos aplicar
	transformaciones al arbol de sintaxis.  Por ejemplo, ciertas 
	optimizaciones del compilador o ciertas reescrituras de pasos 
	anteriores a la generación de código.
	'''
	def generic_visit(self,node):
		
		for field in getattr(node, "_fields"):
			value = getattr(node,field, None)
			if isinstance(value, list):
				newvalues = []
				for item in value:
					if isinstance(item, AST):
						newnode = self.visit(item)
						if newnode is not None:
							newvalues.append(newnode)
					else:
						
						newvalues.append(n)
				value[:] = newvalues
			elif isinstance(value, AST):
				newnode = self.visit(value)
				if newnode is None:
					delattr(node, field)
				else:
					setattr(node, field, newnode)
		return node
		
# NO MODIFICAR
def flatten(top):
	'''
	Aplana el arbol de sintaxis dentro de una lista para efectos
	de depuración y pruebas.  Este retorna una lista de tuplas de
	la forma (depth, node) donde depth es un entero representando
	la profundidad del arból de sintaxis y node es un node AST
	asociado.
	'''
	
	class Flattener(NodeVisitor):
		def __init__(self):
			self.depth = 0
			self.nodes = []
		def generic_visit(self,node):
			self.nodes.append((self.depth,node))
			self.depth += 1
			NodeVisitor.generic_visit(self,node)
			self.depth -= 1
			
	d = Flattener()
	d.visit(top)
	return d.nodes
