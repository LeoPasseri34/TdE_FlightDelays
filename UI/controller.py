import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDDAeroportoP = None
        self._choiceDDAeroportoD = None

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def handleAnalizza(self, e):
        cMinTxt = self._view._txtInCmin.value
        if cMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserire un valore numerico"))
            return
        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Il valore inserito non è un intero"))
            return

        if cMin <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserire un intero positivo"))
            return

        self._model.buildGraph(cMin)
        allNodes = self._model.getAllNodes()
        self.fillDD(allNodes)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.update_page()

    def handleConnessi(self, e):
        if self._choiceDDAeroportoP == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, selezionare una voce dal menu"))
            return
        viciniTuple = self._model.getSortedNeighbours(self._choiceDDAeroportoP)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Di seguito i vicini di questo nodo:"))
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]} - peso: {v[1]}"))
        self._view.update_page()

    def handleCerca(self, e):
        pass

    def fillDD(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self.pickDDPartenza))
            self._view._ddAeroportoD.options.append(
                ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self.pickDDDestinazione))


    def pickDDPartenza(self, e):
        self._choiceDDAeroportoP = e.control.data
        print("pick di partenza called: ", self._choiceDDAeroportoP)

    def pickDDDestinazione(self, e):
        self._choiceDDAeroportoD = e.control.data
        print("pick di destinazione called: ", self._choiceDDAeroportoD)


    def handlePercorso(self,e):
        if self._choiceDDAeroportoP == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, selezionare una voce dal menu come partenza."))
            return
        if self._choiceDDAeroportoD == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, selezionare una voce dal menu come destinazione."))
            return

        path = self._model.getPath(self._choiceDDAeroportoP, self._choiceDDAeroportoD)
        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Cammino fra {self._choiceDDAeroportoP} e {self._choiceDDAeroportoD} non trovato"))
            return
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino fra {self._choiceDDAeroportoP} e {self._choiceDDAeroportoD} trovato! Di seguito i nodi del cammino:"))
            for p in path:
                self._view.txt_result.controls.append(
                    ft.Text(p))
        self._view.update_page()