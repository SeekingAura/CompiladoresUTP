# coding: utf-8
'''
Proyecto 4 - Parte 1
====================
La generación de código para MiniGo. En este proyecto, se va a convertir
el AST en código de maquina intermedio conocido como Asignación estática
única (SSA - Single Static Assignment).
Hay algunas partes importantes que usted necesita hacer para este 
trabajo.  Por favor, lea cuidadosamente antes de empezar:

Asignación Estática ünica
=========================
El primer problema es como descomponer expresiones complejas en algo que
se pueda manejar mas simplemente. Una forma de hacer esto es descomponer
todas las expresiones en una secuencia de asignaciones sencillas que
involucre operaciones binarias o unarias.
Como un ejemplo, supongase que se tiene una expresión matemática igual a
esto:

	2 + 3*4 - 5

Esto es una manera posible de descomponer la expresión en operaciones
simples:

	int_1 = 2
	int_2 = 3
	int_3 = 4
	int_4 = int_2 * int_3
	int_5 = int_1 + int_4
	int_6 = 5
	int_7 = int_5 - int_6

En este código, las variables int_n son simplemente temporales
utilizadas en el ejercicio del cálculo. Una característica crítica de 
SSA es que tales varibles temporales son solamente asignadas una sola 
vez (asignación única) y nunca reutilizadas. Por lo tanto, si se fuera
a evaluar otra expresión, sólo tendría que seguir incrementando los 
números. Por ejemplo, si se evaluara 10+20+30, se tendría código como 
este:

	int_8 = 10
	int_9 = 20
	int_10 = int_8 + int_9
	int_11 = 30
	int_12 = int_11 + int_11

SSA tiene la intensión de imitar las instrucciones de bajo-nivel que se
podría llevar a cabo en una CPU. Por ejemplo, las instrucciones 
anteriores pueden ser traducidas a instrucciones de máquina de 
bajo-nivel (para una CPU hipotética) de esta manera:

	MOVI #2, R1
	MOVI #3, R2
	MOVI #4, R3
	MUL R2, R3, R4
	ADD R4, R1, R5
	MOVI #5, R6
	SUB R5, R6, R7

Otro beneficio de SSA es que es muy fácil de codificar y manipular 
usando estrusturas de datos simples como tuplas. Por ejemplo, se podría
codifica la secuencia anterior de operaciones como una lista como esto:

	[ 
		('movi', 2, 'int_1'),
		('movi', 3, 'int_2'),
		('movi', 4, 'int_3'),
		('mul', 'int_2', 'int_3', 'int_4'),
		('add', 'int_1', 'int_4', 'int_5'),
		('movi', 5, 'int_6'),
		('sub', 'int_5','int_6','int_7'),
	]

Tratando con Variables
======================
En su programa, probablemente va a tener algunas variables que usará y 
le asignará diferentes valores. Por ejemplo:

	a = 10 + 20;
	b = 2 * a;
	a = a + 1;

En "SSA puro", todas las variables en realidad serán versionadas como 
las temporales en las anteriores expresiones. Por ejemplo, tendía que 
emitir código como este:

	int_1 = 10
	int_2 = 20
	a_1 = int_1 + int_2
	int_3 = 2
	b_1 = int_3 * a_1
	int_4 = 1 
	a_2 = a_1 + int_4
	...

Por razones que tendrá sentido más adelante, vamos a tratar las 
variables declaradas como localizaciones de memoria y acceder a ellas 
usando las instrucciones load/store. Por ejemplo:

	int_1 = 10
	int_2 = 20
	int_3 = int_1 + int_2
	store(int_3, "a")
	int_4 = 2
	int_5 = load("a")
	int_6 = int_4 * int_5
	store(int_6,"b")
	int_7 = load("a")
	int_8 = 1
	int_9 = int_7 + int_8
	store(int_9, "a")

Una Palabra a cerca de Tipos
============================
A bajo nivel, las CPUs solamente pueden operar con unos pocos tipos
de datos tales como ints y floats. Debido a que la semántica de los
tipos de bajo-nivel pueden variar un poco, se tendrá que tomar algunas
medidas para manejarlos por separado.

En nuestro código intermedio, simplemente se etiquetará los nombres
de variables temporales y las instrucciones con un tipo asociado de
bajo-nivel. Por ejemplo:

	2 + 3*4 (ints)
	2.0 + 3.0*4.0 (floats)

El código intermedio generado podría lucir como esto:

	('literal_int', 2, 'int_1')
	('literal_int', 3, 'int_2')
	('literal_int', 4, 'int_3')
	('mul_int', 'int_2', 'int_3', 'int_4')
	('add_int', 'int_1', 'int_4', 'int_5')
	('literal_float', 2.0, 'float_1')
	('literal_float', 3.0, 'float_2')
	('literal_float', 4.0, 'float_3')
	('mul_float', 'float_2', 'float_3', 'float_4')
	('add_float', 'float_1', 'float_4', 'float_5')

Nota: Estos tipos pueden o no corresponder directamente a los nombres
de tipos usados en el programa de entrada. Por ejemplo, durante la
traducción, las estructuras de datos de nivel superior se reducirán
a unas operaciones de bajo-nivel.

Su Tarea
========
Su tarea es la siguiente: Escriba una clase Visitor() de AST que tome
un script lola y lo aplane a una secuencia única de instrucciones
de código SSA representado como tuplas de la forma

	(operacion, operandos, ..., destinacion)

Para empezar, su código SSA sólo debe contener las siguientes 
operaciones:

	('alloc_type',varname) # Allocate a variable of a given type
	('literal_type', value, target) # Load a literal value into target
	('load_type', varname, target) # Load the value of a variable into target
	('store_type',source, varname) # Store the value of source into varname
	('add_type', left, right, target ) # target = left + right
	('sub_type',left,right,target) # target = left - right
	('mul_type',left,right,target) # target = left * right
	('div_type',left,right,target) # target = left / right (integer truncation)
	('uadd_type',source,target) # target = +source
	('uneg_type',source,target) # target = -source
	('print_type',source) # Print value of source
'''
import lolaast
import lolablock
from collections import defaultdict

# PASO 1: Mapee los nombres de los operadores símbolos tales 
# como +, -, *, / a los nombres actuales de opcode 'add', 'sub', 
# 'mul', 'div' a ser emitidos en el código SSA. Esto es fácil de hacer
# usando diccionarios:

binary_ops = {
	'+' : 'add',
	'-' : 'sub',
	'*' : 'mul',
	'/' : 'div',
}

unary_ops = {
	'+' : 'uadd',
	'-' : 'usub'
}

# paso 2: Implemente la siguiente clase Node Visitor para que cree una
# secuencia de instrucciones SSA en forma de tuplas. Utilice la
# descripción anterior de los op-codes permitidos como una guía.

class GenerateCode(mgoast.NodeVisitor):
	'''
	Clase Node visitor que crea secuencia de instrucciones codificadas
	3-direcciones.
	'''
	def __init__(self):
		super(GenerateCode, self).__init__()

		# diccionario de versiones para temporales
		self.versions = defaultdict(int)

		# El código generado (lista de tuplas)
		self.code = []

		# Una lista de declaraciones externas (y tipos)
		self.externs = []

	def new_temp(self, typeobj):
		'''
		Crea una variable temporal del tipo dado
		'''
		name = "__%s_%d" % (typeobj.name, self.versions[typeobj.name])
		self.versions[typeobj.name] += 1
		return name

	# Debe implementar métodos visit_Nodename para todos los otros 
	# nodos AST. En su código, tendrá que crear las instrucciones
	# y agregarlas a la lista self.code.

	# Siguen algunos métodos de muestra. Deberá de ajustarlos dependiendo
	# de los nombres de los nodos AST que haya definido.

	def visit_Literal(self, node):
		# Crea un nuevo nombre de variable temporal
		target = self.new_temp(node.type)

		# Cree opcode SSA y agregelo a lista de instrucciones generadas
		inst = ('literal_'+node.type.name, node.value, target)
		self.code.append(inst)

		# Grabe nombre de variable temporal donde el valor fue colocado
		node.gen_location = target

	def visit_BinaryOp(self, node):
		# Visite las expresiones izquierda y derecha
		self.visit(node.left)
		self.visit(node.right)

		# Cree una nueva temporal para guardar el resultado
		target = self.new_temp(node.type)

		# Cree el opcode y agregelo a la lista
		opcode = binary_ops[node.op] + "_" + node.left.type.name
		inst = (opcode, node.left.gen_location, node.right.gen_location, target)
		self.code.append(inst)

		# Almacene la localización del resultado en el node
		node.gen_location = target

	def visit_PrintStatement(self, node):
		# Visite la expresión impresa
		self.visit(node.expr)

		# Cree el opcode y agregelo a la lista
		inst = ('print_'+node.expr.type.name, node.expr.gen_location)
		self.code.append(inst)

	def visit_Program(self,node):
		self.visit(node.program)

	#def visit_Statements(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)

	#def visit_Statement(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)

	def visit_ConstDeclaration(self,node):
		# localice en memoria
		inst = ('alloc_'+node.type.name, node.id)
		self.code.append(inst)

		# almacene el val inicial
		self.visit(node.value)
		inst = ('store_'+node.type.name,
		node.value.gen_location, node.id)
		self.code.append(inst)

	def visit_VarDeclaration(self,node):
		# localice en memoria
		inst = ('alloc_'+node.type.name, node.id)
		self.code.append(inst)
		# almacene pot. val inicial
		if node.value:
			self.visit(node.value)
			inst = ('store_'+node.type.name, node.value.gen_location, node.id)
			self.code.append(inst)

	def visit_LoadLocation(self,node):
		target = self.new_temp(node.type)
		inst = ('load_'+node.type.name, node.name, target)
		self.code.append(inst)
		node.gen_location = target

	#def visit_Extern(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)

	#def visit_FuncPrototype(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)

	#def visit_Parameters(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)
	# node.gen_location = target

	#def visit_ParamDecl(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)

	def visit_AssignmentStatement(self,node):
		self.visit(node.value)

		inst = ('store_'+node.value.type.name, node.value.gen_location, node.location)
		self.code.append(inst)

	def visit_UnaryOp(self,node):
		self.visit(node.left)
		target = self.new_temp(node.type)
		opcode = unary_ops[node.op] + "_" + node.left.type.name
		inst = (opcode, node.left.gen_location)
		self.code.append(inst)
		node.gen_location = target

	def visit_IfStatement(self,node):
		pass

	#def visit_Group(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)

	#def visit_FunCall(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)

	#def visit_ExprList(self,node):
	# self.visit(node.expr)
	# inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	# self.code.append(inst)


# PASO 3: Pruebas
#
# Trate de correr este programa con el archivo de entrada 
# Project4/Tests/good.g y vea el resultado de la secuencia de 
# código SSA.
#
# bash % python mgocode.py good.g
# ... mire la salida ...
#
# 
# Salidas de ejemplo pueden encontrarse en Project4/Tests/good.out. 
# Mientras esté codificando, podrá desear romper el código en partes
# mas manejables.  Piense en pruebas unitarias.

# ---------------------------------------------------------------------
# NO MODIFIQUE NADA DE LO DE ABAJO
# ---------------------------------------------------------------------
def generate_code(node):
	'''
	Genera código SSA desde el nodo AST suministrados
	'''
	gen = GenerateCode()
	gen.visit(node)
	return gen

if __name__ == '__main__':
	import lolalex
	import lolaparse
	import lolacheck
	import sys
	from errors import subscribe_errors, errors_reported

	lexer = golex.make_lexer()
	parser = goparse.make_parser()
	with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
		program = parser.parse(open(sys.argv[1]).read())

		# Comprueba el programa
		gocheck.check_program(program)

		# Si no se han producido errores, genere código
		if not errors_reported():
			code = generate_code(program)
			# Emitir la secuencia de código
			for inst in code.code:
				print(inst)
