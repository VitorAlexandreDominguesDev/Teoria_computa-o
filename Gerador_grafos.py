import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkinter import filedialog
import time


class GraphGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Editor")

        self.graph = nx.Graph()

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas_ntk = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_ntk.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.add_label = tk.Label(master, text="Vértice:")
        self.add_label.pack()
        self.add_entry = tk.Entry(master)
        self.add_entry.pack()
        self.add_button = tk.Button(master, text="Adicionar Vértice", command=self.add_vertex)
        self.add_button.pack()

        self.remove_label = tk.Label(master, text="Vértice a Remover:")
        self.remove_label.pack()
        self.remove_entry = tk.Entry(master)
        self.remove_entry.pack()
        self.remove_button = tk.Button(master, text="Remover Vértice", command=self.remove_vertex)
        self.remove_button.pack()

        self.edge_label = tk.Label(master, text="Aresta (Origem-Destino):")
        self.edge_label.pack()
        self.edge_origin_entry = tk.Entry(master)
        self.edge_origin_entry.pack()
        self.edge_dest_entry = tk.Entry(master)
        self.edge_dest_entry.pack()
        self.edge_weight_label = tk.Label(master, text="Peso:")
        self.edge_weight_label.pack()
        self.edge_weight_entry = tk.Entry(master)
        self.edge_weight_entry.pack()
        self.edge_button = tk.Button(master, text="Adicionar Aresta", command=self.add_edge)
        self.edge_button.pack()

        self.load_button = tk.Button(master, text="Carregar Grafo", command=self.load_graph)
        self.load_button.pack()

        self.save_button = tk.Button(master, text="Salvar Grafo", command=self.save_graph)
        self.save_button.pack()

        self.percorrer_vertices = tk.Button(master, text="Percorrer Vértices", command=self.percorrer_vertices)
        self.percorrer_vertices.pack()

        self.percorrer_arestas = tk.Button(master, text="Percorrer Arestas", command=self.percorrer_arestas)
        self.percorrer_arestas.pack()

        self.prim_button = tk.Button(master, text="Calcular MST (Prim)", command=self.calculate_prim)
        self.prim_button.pack()

        self.boruvka_button = tk.Button(master, text="Calcular MST (Borůvka)", command=self.calculate_boruvka)
        self.boruvka_button.pack()

        self.draw_graph()

    def add_vertex(self):
        vertex = self.add_entry.get()
        if vertex:
            self.graph.add_node(vertex)
            self.draw_graph()
            self.add_entry.delete(0, tk.END)

    def remove_vertex(self):
        vertex = self.remove_entry.get()
        if vertex:
            if vertex in self.graph.nodes():
                self.graph.remove_node(vertex)
                self.draw_graph()
            else:
                print("Vértice não encontrado.")
            self.remove_entry.delete(0, tk.END)

    def add_edge(self):
        origin = self.edge_origin_entry.get()
        dest = self.edge_dest_entry.get()
        weight = self.edge_weight_entry.get()
        if origin and dest and weight:
            self.graph.add_edge(origin, dest, weight=float(weight))
            self.draw_graph()
            self.edge_origin_entry.delete(0, tk.END)
            self.edge_dest_entry.delete(0, tk.END)
            self.edge_weight_entry.delete(0, tk.END)

    def load_graph(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            df = pd.read_csv(filename)
            self.graph = nx.from_pandas_edgelist(df, 'Origem', 'Destino', ['Peso'])
            for u, v, data in self.graph.edges(data=True):
                data['weight'] = float(data['Peso'])
            self.draw_graph()

    def save_graph(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            edges = self.graph.edges(data=True)
            df = pd.DataFrame([(u, v, d['weight']) for u, v, d in edges], columns=['Origem', 'Destino', 'Peso'])
            df.to_csv(filename, index=False)

    def draw_graph(self):
        self.ax.clear()
        pos = nx.planar_layout(self.graph)
        nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_size=500, node_color='skyblue')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
        self.canvas_ntk.draw()

    def percorrer_vertices(self):
        print("Percorrer Vértices")
        percorridos = []
        for vertice in self.graph.nodes():
            print(f"Percorrendo vértice: {vertice}")
            self.ax.clear()
            cor = ["red" if node in percorridos else 'skyblue' for node in list(self.graph.nodes())]
            cor[list(self.graph.nodes()).index(vertice)] = 'red'
            nx.draw(self.graph, nx.planar_layout(self.graph), ax=self.ax, with_labels=True, node_size=500, node_color=cor)
            nx.draw_networkx_edge_labels(self.graph, nx.planar_layout(self.graph), edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
            self.canvas_ntk.draw()
            self.master.update_idletasks()
            time.sleep(1)
            percorridos.append(vertice)
        cor = ['skyblue' for node in self.graph.nodes()]
        nx.draw(self.graph, nx.planar_layout(self.graph), ax=self.ax, with_labels=True, node_size=500, node_color=cor)
        nx.draw_networkx_edge_labels(self.graph, nx.planar_layout(self.graph), edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
        self.canvas_ntk.draw()

    def percorrer_arestas(self):
        print("Percorrer Arestas")
        percorridos = []
        for edge in self.graph.edges(data=True):
            print(f"Percorrendo aresta: {edge[0]} - {edge[1]}")
            self.ax.clear()
            edge_colors = ['red' if (u, v) in percorridos or (v, u) in percorridos else 'black' for u, v in self.graph.edges()]
            edge_colors[list(self.graph.edges()).index((edge[0], edge[1]))] = 'red'
            nx.draw(self.graph, nx.planar_layout(self.graph), ax=self.ax, with_labels=True, node_size=500, node_color='skyblue', edge_color=edge_colors)
            nx.draw_networkx_edge_labels(self.graph, nx.planar_layout(self.graph), edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
            self.canvas_ntk.draw()
            self.master.update_idletasks()
            time.sleep(1)
            percorridos.append((edge[0], edge[1]))
        edge_colors = ['black' for u, v in self.graph.edges()]
        nx.draw(self.graph, nx.planar_layout(self.graph), ax=self.ax, with_labels=True, node_size=500, node_color='skyblue', edge_color=edge_colors)
        nx.draw_networkx_edge_labels(self.graph, nx.planar_layout(self.graph), edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
        self.canvas_ntk.draw()

    def calculate_prim(self):
        if not self.graph.nodes:
            print("Grafo vazio.")
            return
        
        mst = nx.Graph()
        mst.add_nodes_from(self.graph.nodes(data=True))
        visited = set()
        edges = list(self.graph.edges(data=True))
        pos = nx.planar_layout(self.graph)
        
        # Start with an arbitrary node (assuming the graph is not empty)
        start_node = next(iter(self.graph.nodes))
        visited.add(start_node)
        
        while len(visited) < len(self.graph.nodes):
            # Find minimum weight edge connecting visited and unvisited nodes
            edge = min((e for e in edges if (e[0] in visited and e[1] not in visited) or 
                                        (e[1] in visited and e[0] not in visited)),
                    key=lambda x: x[2]['weight'])
            
            edges.remove(edge)
            if edge[0] in visited:
                mst.add_edge(edge[0], edge[1], weight=edge[2]['weight'])
                visited.add(edge[1])
            else:
                mst.add_edge(edge[1], edge[0], weight=edge[2]['weight'])
                visited.add(edge[0])
            
            # Update visualization
            self.ax.clear()
            node_colors = ['red' if n in visited else 'skyblue' for n in self.graph.nodes]
            edge_colors = ['red' if (u, v) in mst.edges or (v, u) in mst.edges else 'black' for u, v in self.graph.edges]
            nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_size=500, node_color=node_colors, edge_color=edge_colors)
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
            self.canvas_ntk.draw()
            self.master.update_idletasks()
            time.sleep(1)
        
        self.ax.clear()
        nx.draw(mst, pos, ax=self.ax, with_labels=True, node_size=500, node_color='lightgreen')
        nx.draw_networkx_edge_labels(mst, pos, edge_labels=nx.get_edge_attributes(mst, 'weight'))
        self.canvas_ntk.draw()


    def calculate_boruvka(self):
        def boruvka_step(graph):
            components = list(nx.connected_components(graph))
            cheapest_edges = {}
            for component in components:
                min_edge = None
                for node in component:
                    for neighbor, data in graph[node].items():
                        if neighbor not in component:
                            if min_edge is None or data['weight'] < graph[min_edge[0]][min_edge[1]]['weight']:
                                min_edge = (node, neighbor)
                if min_edge:
                    cheapest_edges[component] = min_edge
            return [(u, v, graph[u][v]['weight']) for u, v in cheapest_edges.values()]

        mst = nx.Graph()
        mst.add_nodes_from(self.graph.nodes(data=True))
        pos = nx.planar_layout(self.graph)

        while len(mst.edges) < len(self.graph.nodes) - 1:
            new_edges = boruvka_step(self.graph)
            mst.add_weighted_edges_from(new_edges)
            
            for u, v, data in new_edges:
                self.graph.remove_edge(u, v)
                
                # Atualizando a visualização
                self.ax.clear()
                node_colors = ['red' if n in mst.nodes else 'skyblue' for n in self.graph.nodes]
                edge_colors = ['red' if (u, v) in mst.edges or (v, u) in mst.edges else 'black' for u, v in self.graph.edges]
                nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_size=500, node_color=node_colors, edge_color=edge_colors)
                nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
                self.canvas_ntk.draw()
                self.master.update_idletasks()
                time.sleep(1)

        self.ax.clear()
        nx.draw(mst, pos, ax=self.ax, with_labels=True, node_size=500, node_color='lightgreen')
        nx.draw_networkx_edge_labels(mst, pos, edge_labels=nx.get_edge_attributes(mst, 'weight'))
        self.canvas_ntk.draw()

def main():
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
