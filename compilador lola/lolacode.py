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
import ast_lola as ast
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

class GenerateCode(ast.NodeVisitor):
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
		self.stackBuild=[]
		self.stackExprOp=[]
		self.stackTermOp=[]
		self.stackValues=[]
		self.valueVisit=0
	def new_temp(self, typeobj):
		'''
		Crea una variable temporal del tipo dado
		'''
		name = "__%s_%d" % (typeobj, self.versions[typeobj])
		self.versions[typeobj] += 1
		return name

	# Debe implementar métodos visit_Nodename para todos los otros 
	# nodos AST. En su código, tendrá que crear las instrucciones
	# y agregarlas a la lista self.code.

	# Siguen algunos métodos de muestra. Deberá de ajustarlos dependiendo
	# de los nombres de los nodos AST que haya definido.
	
	def visit_Modulo(self, node):
		# Crea un nuevo nombre de variable temporal
		target = self.new_temp(node.tipo)

		# Cree opcode SSA y agregelo a lista de instrucciones generadas
		inst = ('Build_'+node.tipo, node.ID1, target)
		self.code.append(inst)

		# Grabe nombre de variable temporal donde el valor fue colocado
		node.gen_location = target
		#print("location", target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
			#elif(value is not None):#ramas...

			
		
	
	def visit_DeclaracionTipo(self, node):
		#print("generico")
		# Crea un nuevo nombre de variable temporal
		target = self.new_temp(node.tipo)

		# Cree opcode SSA y agregelo a lista de instrucciones generadas
		inst = ('Build_'+node.tipo, node.ID1, target)
		self.code.append(inst)

		# Grabe nombre de variable temporal donde el valor fue colocado
		node.gen_location = target
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
			#elif(value is not None):#ramas...
			
		
		
	def visit_ListaId(self, node):
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
			#elif(value is not None):#ramas...
		# Crea un nuevo nombre de variable temporal
		
		node.gen_location = []
		for IDs in node.idsListaId:
			target = self.new_temp(node.tipo)
			# Cree opcode SSA y agregelo a lista de instrucciones generadas
			inst = ('BuildPort_'+node.tipo, IDs, target)
			self.code.append(inst)

			# Grabe nombre de variable temporal donde el valor fue colocado
			node.gen_location.append(target)
			
			self.stackBuild.append([IDs, target])
		
	def visit_TipoFormal(self, node):
		node.gen_location = []
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				#print(value)
				self.visit(value)
			elif value is None:
				
				for value in self.stackBuild:
					target = self.new_temp("SET-SIZE")
					# Cree opcode SSA y agregelo a lista de instrucciones generadas
					inst = ('SetPortSize_'+value[1][2:-2], [value[1][2:], '1'], target)
					self.code.append(inst)

					# Grabe nombre de variable temporal donde el valor fue colocado
					node.gen_location.append(target)
		node.gen_location = []
		for value in self.stackBuild:
			target = self.new_temp("SET-TYPE")
			# Cree opcode SSA y agregelo a lista de instrucciones generadas
			inst = ('SetPortType_'+value[1][2:-2], [value[1][2:], 'BIT'], target)
			self.code.append(inst)

			# Grabe nombre de variable temporal donde el valor fue colocado
			node.gen_location.append(target)
			
			#elif(value is not None):#ramas...
		self.stackBuild=[]
	
	def visit_ExpresionCorcheteOR(self, node):
		node.gen_location = []
		#print("pase or")
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						for value in self.stackBuild:
							target = self.new_temp("SET-SIZE")
							# Cree opcode SSA y agregelo a lista de instrucciones generadas
							inst = ('SetPortSize_'+value[1][2:-2], [value[1][2:], str(self.valueVisit)], target)
							self.code.append(inst)
					elif item is None:
						for value in self.stackBuild:
							target = self.new_temp("SET-SIZE")
							# Cree opcode SSA y agregelo a lista de instrucciones generadas
							inst = ('SetPortSize_'+value[1][2:-2], [value[1][2:], 'INF'], target)
							self.code.append(inst)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
				

			# Grabe nombre de variable temporal donde el valor fue colocado
	def visit_FactorValor(self, node):
		node.gen_location = []
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
			elif value is not None:
				#print(value)
				self.valueVisit=value
	def visit_FactorSelector(self, node):
		node.gen_location = []
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
			
		self.valueVisit=node.ID
		
	
	
	def visit_Tipo(self, node):
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
			elif value is None:
				for valueStack in self.stackBuild:
					#print("yolo", value)
					target = self.new_temp("SET-SIZE")
					# Cree opcode SSA y agregelo a lista de instrucciones generadas
					inst = ('SetPortSize_'+valueStack[1][2:-2], [valueStack[1][2:], "1"], target)
					self.code.append(inst)
	
	def visit_TipoSimpleID(self, node):
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
			
		for valueStack in self.stackBuild:
			#print("yolo", value)
			target = self.new_temp("SET-SIZE")
			# Cree opcode SSA y agregelo a lista de instrucciones generadas
			inst = ('SetPortSize_'+valueStack[1][2:-2], [valueStack[1][2:], "1"], target)
			self.code.append(inst)
	def visit_TipoSimpleBasico(self, node):
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if value is not None:
				for valueStack in self.stackBuild:
					#print("yolo", value)
					target = self.new_temp("SET-TYPE")
					# Cree opcode SSA y agregelo a lista de instrucciones generadas
					inst = ('SetPortType_'+valueStack[1][2:-2], [valueStack[1][2:], str(value)], target)
					self.code.append(inst)
				self.stackBuild=[]
	
	def visit_DeclaracionConstante(self, node):
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
			elif value is not None:
				target = self.new_temp(node.tipo)
				# Cree opcode SSA y agregelo a lista de instrucciones generadas
				inst = ('BuildConst_'+node.tipo, value, target)
				self.code.append(inst)
				#self.stackBuild.append([value, target])
		
		targetBefore=target[2:]
		target = self.new_temp("SET-VALUE-CONST")
		# Cree opcode SSA y agregelo a lista de instrucciones generadas
		inst = ('SetValueConst_'+node.tipo, [targetBefore, self.valueVisit], target)
		self.code.append(inst)
		
	def visit_Asignacion(self, node):
		self.stackExprOp=[]
		self.stackTermOp=[]		
		self.stackValues=[]
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
		op1=None
		firstResult=None
		op=[]
		opunary=None
		
		lastResult=None
		pos=0
		#binary_ops
		#print("aca", self.stackValues)
		lenlist=len(self.stackValues)
		listValues=self.stackValues
		self.stackValues=iter(self.stackValues)
		for enum, value in enumerate(self.stackValues):
			#print("valor", value)
			if(value=="*"):
				op.append(value)
			elif(op1 is None):
				#print("yolo", value)
				for findValue in self.code:
					#print("checando op1", findValue[1], value)
					if(value==findValue[1]):
						#print("bingo", findValue[2])
						op1=findValue[2]
			elif(firstResult is None and value is not None):
					for findValue in self.code:
						if(value==findValue[1]):
							#print("bongodo", findValue[2])
							firstResult=findValue[2]
			elif(value is None and len(op)>0):
			
				for operation in op:
					target = self.new_temp(node.tipo+"_"+binary_ops[operation])
					# Cree opcode SSA y agregelo a lista de instrucciones generadas
					inst = (binary_ops[operation]+'_'+node.tipo, [op1, firstResult], target)
					self.code.append(inst)
					firstResult=target
					#self.stackBuild.append([value, target])
					try:
						if(listValues[enum+1]!="*"):
							nextoperation=next(self.stackValues)
						else:
							nextoperation=None
					except:
						nextoperation=None
					if(nextoperation is not None):
						for findValue in self.code:
							if(value==findValue[1]):
								op1=findValue[2]
					elif(nextoperation is None):
						op=[]
						if(lastResult is None):
							lastResult=firstResult
						else:
							#print("ay!")
							if(len(self.stackExprOp)>0):
								opunary=self.stackExprOp.pop(0)
							target = self.new_temp(node.tipo+"_"+binary_ops[opunary])
							# Cree opcode SSA y agregelo a lista de instrucciones generadas
							inst = (binary_ops[opunary]+'_'+node.tipo, [lastResult, firstResult], target)
							self.code.append(inst)
							lastResult=target
							
						firstResult=None
						op1=None
			else:
				#print("aqui estoy", value)
				
				if(len(self.stackExprOp)>0):
					opunary=self.stackExprOp.pop(0)
				if(lastResult is None):
					try:
						
						value=next(self.stackValues)
						for findValue in self.code:
							if(value==findValue[1]):
								lastResult=findValue[2]
						temp=lastResult
						lastResult=op1
						op1=temp
						#print("en otra parte", lastResult)
					except:
						lastResult=None
						
				if(opunary is not None):
					target = self.new_temp(node.tipo+"_"+binary_ops[opunary])
					# Cree opcode SSA y agregelo a lista de instrucciones generadas
					inst = (binary_ops[opunary]+'_'+node.tipo, [lastResult, op1], target)
					self.code.append(inst)
					lastResult=target
					#firstResult=None
					op1=None
		result=None
		if(lenlist>2):
			for findValue in self.code:
				#print("checando op1", findValue[1], value)
				if(node.ID==findValue[1]):
					#print("bingo", findValue[2])
					result=findValue[2]
			
			target = self.new_temp(node.tipo+"_MOV")
			# Cree opcode SSA y agregelo a lista de instrucciones generadas
			inst = ('mov_'+node.tipo, [self.code[len(self.code)-1][2], result], target)
			self.code.append(inst)
		self.stackExprOp=[]
		self.stackTermOp=[]		
		self.stackValues=[]
	def visit_Expresion(self, node):
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					elif(item is not None):#caso de ramas
							self.stackExprOp.append(item)
		
	def visit_Termino(self, node):
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.stackValues.append(self.valueVisit)
					elif(item is not None):#caso de ramas
							self.stackValues.append(item)
		self.stackValues.append(None)
		
	def generic_visit(self, node):
		#print("generico")
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
					#elif(item is not None):#caso de ramas
			elif isinstance(value, ast.AST):
				self.visit(value)
			#elif(value is not None):#ramas...
			
	
	
	
	
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
