# Lola - Dibujar AST + graphviz

import pydotplus as pgv
import ast_lola    as ast

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
		#self.ModulosContenido=[]
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
		#visita los hijos, por decirlo de algun modo...
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, AST):
						self.visit(item)
					else:#caso de ramas
						targetHijo = self.new_node(None, value)
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif isinstance(value, AST):
				self.visit(value)
		self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		
	
	def visit_Modulo(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		targetHijo=self.visit(hijo)
		self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
	
		

