# Lola - Dibujar AST + graphviz

import pydotplus as pgv
import ast_lola as ast
import operator

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.truediv,
        '%' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(op1, operator, op2):
    op1,op2 = int(op1), int(op2)
    return get_operator_fn(operator)(op1, op2)
	
class DotCode(ast.NodeVisitor):
	'''
	Clase Node Visitor que crea secuencia de instrucciones Dot
	'''
	
	def __init__(self):
		super(DotCode, self).__init__()
		
		# Secuencia para los nombres de nodos
		self.id = 0
		
		# Stack para retornar nodos procesados
		self.stack = []
		
		# Inicializacion del grafo para Dot
		self.dot = pgv.Dot('AST', graph_type='digraph')  
		
		self.dot.set_node_defaults(shape='box', color='lightgray', style='filled')
		self.dot.set_edge_defaults(arrowhead='none')
		
		#control de chequeo de variables
		self.DeclarandoVariables=None
		self.VisitandoModulo=None
		
		self.types=[]
		self.typesIDs=[]
		self.typesArrays=[]
		
		self.moduleIDs=[]
		self.moduleArrays=[]
		
		self.StartOperation=False
		self.DeclarandoConstante=False
		self.ValueOperation=0
		self.opSimbolExpresion=None
		
	def __repr__(self):
		return self.dot.to_string()
	
	def new_node(self, node, label=None, shape='box'):
		'''
		Crea una variable temporal como nombre del nodo
		'''
		if label is None:
			label = node.__class__.__name__#le entrega al label, es decir nombre el label
		self.id += 1
		return pgv.Node('n{}'.format(self.id), label=label, shape=shape)
	
	def visit_Lola(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		tieneHijos=False
		#visita los hijos, por decirlo de algun modo...
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		
		
	
	def visit_Modulo(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item)
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value)
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		
		self.types=[]
		self.typesIDs=[]
		self.typesArrays=[]
		
		self.moduleIDs=[]
		self.moduleArrays=[]
		self.stack.append(target)
	
	def visit_DeclaracionTipoPuntoComa(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.VisitandoModulo=False
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.VisitandoModulo=True
		self.stack.append(target)
		
	def visit_DeclaracionConstante(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.DeclarandoConstante=True
		self.DeclarandoVariables=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			
			if isinstance(value, ast.AST):
				if(field=="expresion" and not self.VisitandoModulo):
					#print("agrege valor de CONST como ", value)
					#print(self.typesIDs)
					self.typesIDs[len(self.typesIDs)-1][1]=self.visit(value)
					#print(self.typesIDs)
				elif(field=="expresion" and self.VisitandoModulo):
					#print("agrege valor de CONST ", value)
					#print(self.moduleIDs)
					self.moduleIDs[len(self.moduleIDs)-1][1]=self.visit(value)
					#print(self.moduleIDs)
					#seguir aqui
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				if(field=="ID" and not self.VisitandoModulo):
					#print("agrege typesIDs como ", value)
					
					self.typesIDs.append([value, None])
				elif(field=="ID" and self.VisitandoModulo):
					#print("agrege moduleIDs como ", value)
					self.moduleIDs.append([value, None])
					
					
					
				targetHijo = self.new_node(None, value)
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.StartOperation=False
		self.ValueOperation=0
		self.DeclarandoConstante=False
		self.stack.append(target)
	
	
	def visit_Expresion(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			#print("visitando expresion ", value)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						#print("encontre otro valor en expresion", item)
						termvalue=self.visit(item)
						#eval_binary_expr()#verificar
						if(not self.StartOperation):
							self.ValueOperation=termvalue
							self.StartOperation=True
						elif((self.opSimbolExpresion=="+" or self.opSimbolExpresion=="-" or self.opSimbolExpresion=="/" or self.opSimbolExpresion=="MOD") and self.DeclarandoConstante and isinstance(self.ValueOperation, int) and isinstance(termvalue, int)):
							#print("operando %s %s %s" % (self.ValueOperation, self.opSimbolExpresion, termvalue))
							self.ValueOperation=eval_binary_expr(self.ValueOperation, self.opSimbolExpresion, termvalue)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						#print("encontre valor en expresion",item)
						self.opSimbolExpresion=item
						targetHijo = self.new_node(None, item)
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))	
				# targetHijo = self.new_node(None, value)
				# self.dot.add_node(targetHijo)
				# self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
		#print("retorno de nodo expresion", self.ValueOperation)
		return self.ValueOperation
		
	def visit_Termino(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						#print("encontre otro valor en termino",item)
						#print("visitando, ", item)
						termvalue=self.visit(item)
						#eval_binary_expr()
						if(not self.StartOperation):
							self.ValueOperation=termvalue
							self.StartOperation=True
						elif((self.opSimbolExpresion=="+" or self.opSimbolExpresion=="-" or self.opSimbolExpresion=="/" or self.opSimbolExpresion=="MOD") and self.DeclarandoConstante and isinstance(self.ValueOperation, int) and isinstance(termvalue, int)):
							#print(item, self.ValueOperation, termvalue, self.opSimbolExpresion)
							self.ValueOperation=eval_binary_expr(self.ValueOperation, self.opSimbolExpresion, termvalue)
						
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						#print("encontre valor en expresion",item, type(item))
						
						self.opSimbolExpresion=item
						targetHijo = self.new_node(None, item)
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))	
				# targetHijo = self.new_node(None, value)
				# self.dot.add_node(targetHijo)
				# self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
		return self.ValueOperation
	
	def visit_FactorValor(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if(value is not None):
				#print("visit_FactorValor ", value)
				targetHijo = self.new_node(None, value)
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		#print(value)
		self.stack.append(target)
		return value
		
	
	def visit_FactorSelector(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				#print(value)
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
				self.stack.append(target)
				#print("visitando factorselector con ",value, self.VisitandoModulo, self.DeclarandoVariables)
				existValue=True
				if(not self.VisitandoModulo):
					if value not in self.typesIDs:
						existValue=False
						for items in self.typesIDs:
							if(isinstance(items, list)):
								for i in items:
									if(i==value):
										existValue=True
					if(not existValue):
						print("{} no ha sido declarado".format(value))
				elif(self.VisitandoModulo):#verificar esto
					if value not in self.moduleIDs:
						existValue=False
						#termvalue=self.visit(item)
						for items in self.moduleIDs:
							if(isinstance(items, list)):
								for i in items:
									if(i==value):
										existValue=True
					if(not existValue):
						print("{} no ha sido declarado".format(value))
				self.stack.append(target)
				return value
		
		self.stack.append(target)
		#print(value)
		
	
	def visit_ListaId(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item)
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
						if(field=="idsListaId" and not self.VisitandoModulo):
							#print("agrege typesIDs como ", item)
							if item not in self.typesIDs:
								self.typesIDs.append(item)
							else:
								self.typesIDs.remove(item)
								self.typesIDs.append(item)
								print("peligro, redeclarando valor de lista id en type", item)
							#print(self.typesIDs)
						elif(field=="idsListaId" and self.VisitandoModulo):
							#print("agrege moduleIDs como ", item)
							if item not in self.moduleIDs:
								self.moduleIDs.append(item)
							else:
								self.moduleIDs.remove(item)
								self.moduleIDs.add(item)
								print("peligro, redeclarando valor de lista id de modulos", item)
							#print(self.moduleIDs)
							self.moduleIDs.append(item)
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value)
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
		
	def visit_SentenciaSecuenciaBEGIN(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		
		
		self.stack.append(target)
		
		
		
	def generic_visit(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		
		
		self.stack.append(target)
		
		

