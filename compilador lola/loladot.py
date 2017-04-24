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
		
		#self.typesIDs=[]
		self.typePortsIn=[]
		self.typePortsInOut=[]
		self.typePortsOut=[]
		self.typeConst=[]
		
		
		#self.moduleArrays=[]
		self.moduleTypes=[]
		self.modulePortsIn=[]
		self.modulePortsInOut=[]
		self.modulePortsOut=[]
		self.modulePortsVar=[]
		self.moduleConst=[]
		
		self.PortsSize=[]
		self.indexing=[]
		#etiquetas de control
		self.StartOperation=False
		self.DeclarandoConstante=False
		self.ValueOperation=0
		self.opSimbolExpresion=None
		self.TipoFormal=False
		self.PortsIn=False
		self.PortsInOut=False
		self.PortsOut=False
		self.PortsVar=False
		self.usingConst=None
		self.dataType=None
		self.StartAssing=True
		self.selectorValue=None
		
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

	def visit_Modulo(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		
		#self.typesIDs=[]
		self.typesArrays=[]
		#self.typePorts=[[],[],[]]
		#self.moduleIDs=[]
		#self.modulePorts=[[],[],[]]
		self.typePortsIn=[]
		self.typePortsInOut=[]
		self.typePortsOut=[]
		self.typeConst=[]
		
		
		self.moduleArrays=[]
		self.moduleTypes=[]
		self.modulePortsIn=[]
		self.modulePortsInOut=[]
		self.modulePortsOut=[]
		self.moduleConst=[]
		
		self.PortsSize=[]
		self.TipoDato=None
		
		
		self.stack.append(target)
		
	def visit_DeclaracionTipo(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.typePortsIn=[]
		self.typePortsInOut=[]
		self.typePortsOut=[]
		self.typeConst=[]
		self.VisitandoModulo=False
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				if(field=="ID0"):
					self.moduleTypes.append([value, None, None, None, None])
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.VisitandoModulo=True
		self.moduleTypes[len(self.moduleTypes)-1][1]=self.typePortsIn
		self.moduleTypes[len(self.moduleTypes)-1][2]=self.typePortsInOut
		self.moduleTypes[len(self.moduleTypes)-1][3]=self.typePortsOut
		self.moduleTypes[len(self.moduleTypes)-1][4]=self.typeConst
		self.typePortsIn=[]
		self.typePortsInOut=[]
		self.typePortsOut=[]
		self.typeConst=[]
		self.stack.append(target)
		
	def visit_DeclaracionConstante(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.DeclarandoConstante=True
		self.DeclarandoVariables=True
		self.StartOperation=False
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			
			if isinstance(value, ast.AST):
				if(field=="expresion" and not self.VisitandoModulo):
					self.typeConst[len(self.typeConst)-1][1]=self.visit(value)
				elif(field=="expresion" and self.VisitandoModulo):
					self.moduleConst[len(self.moduleConst)-1][1]=self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				if(field=="ID" and not self.VisitandoModulo):
					self.typeConst.append([value, None])
				elif(field=="ID" and self.VisitandoModulo):
					self.moduleConst.append([value, None])
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.StartOperation=False
		self.ValueOperation=0
		self.DeclarandoConstante=False
		self.stack.append(target)
	
	def visit_TipoFormalIN(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.PortsIn=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsIn=False
		self.stack.append(target)
	
	def visit_TipoFormalINOUT(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.PortsInOut=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsInOut=False
		self.stack.append(target)
	
	
	def visit_DeclaracionVariableIN(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.PortsIn=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsIn=False
		self.stack.append(target)
	
	def visit_DeclaracionVariableOUT(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.PortsOut=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsOut=False
		self.stack.append(target)
		
	def visit_DeclaracionVariableVAR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.PortsVar=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsVar=False
		self.stack.append(target)
	
	def visit_TipoFormallistaIdR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.PortsSize=[]
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		
	def visit_TipoFormalINOUT(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.PortsSize=[]
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
	
	
	def visit_DeclaracionVariableRecursivoR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.PortsSize=[]
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		
		
		
	def Tipo(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		
	def TipoExpresionesR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						
						self.PortsSize.append(self.visit(item))
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
	
	def visit_TipoFormal(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.TipoFormal=True
		setup=False
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				if(not self.VisitandoModulo):
					if(self.PortsIn):
						for Ports in self.typePortsIn:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize[0]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports.append(resize)
								Ports.append("BIT")
								
							
					if(self.PortsInOut):
						for Ports in self.typePortsInOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize[0]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports.append(resize)
								Ports.append("BIT")
								
					if(self.PortsOut):
						for Ports in self.typePortsOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize[0]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports.append(resize)
								Ports.append("BIT")
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
				setup=True
		if(not setup):
			
			if(not self.VisitandoModulo):
				if(self.PortsIn):
					for Ports in self.typePortsIn:
						if(Ports[1] is None):
							Ports[1]=1
							Ports.append("BIT")
							#print(Ports)
						
				if(self.PortsInOut):
					for Ports in self.typePortsInOut:
						if(Ports[1] is None):
							Ports[1]=1
							Ports.append("BIT")
				if(self.PortsOut):
					for Ports in self.typePortsOut:
						if(Ports[1] is None):
							Ports[1]=1
							Ports.append("BIT")
		self.TipoFormal=False
		self.stack.append(target)
		
	def visit_TipoFormalBus(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		#self.TipoFormal=True
		setup=False
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				if(not self.VisitandoModulo):
					if(self.PortsIn):
						for Ports in self.typePortsIn:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize[0]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports.append(resize)
								Ports.append("NOTVALUE")
								
							
					if(self.PortsInOut):
						for Ports in self.typePortsInOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize[0]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports.append(resize)
								Ports.append("NOTVALUE")
								
					if(self.PortsOut):
						for Ports in self.typePortsOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize[0]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports.append(resize)
								Ports.append("NOTVALUE")
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
				setup=True
			elif(value is not None):
				if(self.PortsIn):
					for Ports in self.typePortsIn:
						if(Ports[len(Ports)-1]=="NOTVALUE"):
							Ports[len(Ports)-1]==value
						
				if(self.PortsInOut):
					for Ports in self.typePortsInOut:
						if(Ports[len(Ports)-1]=="NOTVALUE"):
							Ports[len(Ports)-1]==value
				if(self.PortsOut):
					for Ports in self.typePortsOut:
						if(Ports[len(Ports)-1]=="NOTVALUE"):
							Ports[len(Ports)-1]==value
				else:
					if(self.PortsIn):
						for Ports in self.typePortsIn:
							if(Ports[len(Ports)-1]=="NOTVALUE"):
								Ports[len(Ports)-1]==value
							
					if(self.PortsInOut):
						for Ports in self.typePortsInOut:
							if(Ports[len(Ports)-1]=="NOTVALUE"):
								Ports[len(Ports)-1]==value
					if(self.PortsOut):
						for Ports in self.typePortsOut:
							if(Ports[len(Ports)-1]=="NOTVALUE"):
								Ports[len(Ports)-1]==value
		
		#self.TipoFormal=False
		self.stack.append(target)
	
	def visit_TipoSimpleBasico(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if(value is not None):#ramas...
				if(not self.VisitandoModulo):
					if(self.PortsIn):
						for Ports in self.typePortsIn:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
								#print(Ports)
							
					if(self.PortsInOut):
						for Ports in self.typePortsInOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
					if(self.PortsOut):
						for Ports in self.typePortsOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
			
				elif(self.VisitandoModulo):
					
					if(self.PortsIn):
						for Ports in self.modulePortsIn:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
								
							
					if(self.PortsInOut):
						for Ports in self.modulePortsInOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
					if(self.PortsOut):
						for Ports in self.modulePortsOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
					
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
	
	def visit_TipoSimpleID(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if(value is not None):#ramas...
				if(self.PortsVar):
					self.modulePortsVar
					for Ports in self.modulePortsVar:
						if(Ports[1] is None):
							Ports[1]=self.PortsSize
							for resize in self.PortsSize:
								Ports[1]=self.PortsSize
							Ports.append(value)
							print(value)
				
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
	
	def visit_ExpresionCorcheteOR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.ValueOperation=None
						self.StartOperation=False
						resize=self.visit(item)
						print("valor resize", resize)
						if(resize is None):
							self.PortsSize.append(-1)
						else:
							self.PortsSize(resize)
						print("valor portssize ", self.PortsSize)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
	
	def visit_ExpresionOpcional(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			
			if isinstance(value, ast.AST):
				resize=self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		return resize
	
	def visit_Expresion(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						termvalue=self.visit(item)
						if(not self.StartOperation):
							self.ValueOperation=termvalue
							self.StartOperation=True
						elif((self.opSimbolExpresion=="+" or self.opSimbolExpresion=="-" or self.opSimbolExpresion=="/" or self.opSimbolExpresion=="MOD") and self.DeclarandoConstante and isinstance(self.ValueOperation, int) and isinstance(termvalue, int)):
							self.ValueOperation=eval_binary_expr(self.ValueOperation, self.opSimbolExpresion, termvalue)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						self.opSimbolExpresion=item
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
		return self.ValueOperation
		
		
	def visit_Termino(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						termvalue=self.visit(item)
						if(not self.StartOperation):
							self.ValueOperation=termvalue
							self.StartOperation=True
						elif((self.opSimbolExpresion=="+" or self.opSimbolExpresion=="-" or self.opSimbolExpresion=="/" or self.opSimbolExpresion=="MOD") and self.DeclarandoConstante and isinstance(self.ValueOperation, int) and isinstance(termvalue, int)):
							self.ValueOperation= eval_binary_expr(self.ValueOperation, self.opSimbolExpresion, termvalue)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
						self.stack.append(target)
						
					elif(item is not None):#caso de ramas
						
						self.opSimbolExpresion=item
						targetHijo = self.new_node(None, item)
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))	
		self.stack.append(target)
		return self.ValueOperation
		
		
	def visit_FactorValor(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if(value is not None):
				targetHijo = self.new_node(None, value)
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
				
		self.stack.append(target)
		return value
		
	
	def visit_FactorSelector(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
				self.stack.append(target)
				existValue=False
				if(not self.VisitandoModulo):
					self.usingConst=None
					for valuei in self.typeConst:
						if(valuei[0]==value):
							self.usingConst=valuei[1]
							existValue=True
					
					if(self.StartAssing):
						for Ports in self.typePortsIn:
							if(Ports[0]==value):
								self.selectorValue=value
								existValue=True
								#print("comparando",Ports[len(Ports)-1],self.dataType)
								if(Ports[len(Ports)-1]!=self.dataType):
									
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
									
						for Ports in self.typePortsInOut:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						for Ports in self.typePortsOut:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								print("Error el puerto de salida debe ser resultado de una asignación, valor", value)
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						
							
					if(not existValue):
						print("{} no ha sido declarado".format(value))
				elif(self.VisitandoModulo):#verificar esto
					self.usingConst=None
					for valuei in self.moduleConst:
						if(valuei[0]==value):
							self.usingConst=valuei[1]
							existValue=True
					
					if(self.StartAssing):
						for Ports in self.modulePortsIn:
							if(Ports[0]==value):
								self.selectorValue=value
								existValue=True
								#print("aqui comparando", Ports[len(Ports)-1],self.dataType)
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
									
						for Ports in self.modulePortsInOut:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						for Ports in self.modulePortsOut:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								print("Error el puerto de salida debe ser resultado de una asignación, valor", value)
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						"""			
						for Ports in self.modulePortsVar:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						"""
					if(not existValue):
						print("{} no ha sido declarado".format(value))
				self.stack.append(target)
				
		
		self.stack.append(target)
		return self.usingConst
		
	
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
						if(not self.VisitandoModulo):
							#print("agrege typesIDs como ", item)
							existValue=False
							pos=None
							#print(item)
							for enum, Ports in enumerate(self.typePortsIn):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.typePortsIn[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de TYPE".format(item))
									
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.typePortsInOut):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.typePortsInOut[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de TYPE".format(item))
								
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.typePortsOut):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.typePortsOut[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de TYPE".format(item))
							if(self.PortsIn):
								self.typePortsIn.append([item, None])
							if(self.PortsInOut):
								self.typePortsInOut.append([item, None])
							if(self.PortsOut):
								self.typePortsOut.append([item, None])
							
							
							
							#print(self.typesIDs)
						elif(self.VisitandoModulo):
							#print("agrege moduleIDs como ", item)
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.modulePortsIn):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.modulePortsIn[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de MODULE".format(item))
									
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.modulePortsInOut):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.modulePortsInOut[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de MODULE".format(item))
								
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.modulePortsOut):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.modulePortsVar):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break		
									
							if(existValue):
								del self.modulePortsOut[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de TYPE".format(item))
							if(self.PortsIn):
								self.modulePortsIn.append([item, None])
							if(self.PortsOut):
								self.modulePortsOut.append([item, None])
							if(self.PortsInOut):
								self.modulePortsInOut.append([item, None])
							if(self.PortsVar):
								self.modulePortsVar.append([item, None])
							#print(self.moduleIDs)
							#self.moduleIDs.append(item)
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value)
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
		
	def visit_SentenciaSecuencia(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.dataType=None
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		
		
		self.stack.append(target)
		
	def visit_Asignacion(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.StartAssing=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				if(field=="ID"):
					if(not self.VisitandoModulo):
						existValue=False
						if(self.StartAssing):
							for valuei in self.typeConst:
								if(valuei[0]==value):
									print("No se puede asignar modos de conexión a una constante, valor", value)
									existValue=True
							for Ports in self.typePortsIn:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									print("error, un puerto de entrada no puede ser resultado, valor", value)
										
							for Ports in self.typePortsInOut:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									self.dataType=Ports[len(Ports)-1]
							for Ports in self.typePortsOut:
								if(Ports[0]==value):
									if(Ports[0]==value):
										#self.selectorValue=value
										existValue=True
										self.dataType=Ports[len(Ports)-1]
										#print("port:",Ports)
										#print("colocando tipo ", self.dataType)
								
						if(not existValue):
							print("{} no ha sido declarado".format(value))
					elif(self.VisitandoModulo):#verificar esto
						existValue=False
						#print("aqui")
						for valuei in self.moduleConst:
							if(valuei[0]==value):
								print("No se puede dar modos de conexión a una constante, valor", value)
						
						if(self.StartAssing):
							for Ports in self.modulePortsIn:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									print("error, un puerto de entrada no puede ser resultado, valor", value)
										
							for Ports in self.modulePortsInOut:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									self.dataType=Ports[len(Ports)-1]
							for Ports in self.modulePortsOut:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									self.dataType=Ports[len(Ports)-1]
									
									
						if(not existValue):
							print("{} no ha sido declarado".format(value))
					
					

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
		
		

