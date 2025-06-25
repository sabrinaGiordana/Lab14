import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        negozio = self._view._ddStore.value
        diff = self._view._txtIntK.value
        if negozio is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un negozio !!!", color="red"))
            self._view.update_page()
            return

        if diff == "":
            self._view.txt_result.controls.append(ft.Text("Inserire un numero di giorni massimo !!!", color="red"))
            self._view.update_page()
            return

        self._model.builtGraph(negozio, diff)
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!!!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {len(self._model._nodes)}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.numArchi()}"))

        self.fillNodi(self._model._nodes)
        self._view.update_page()


    def handleCerca(self, e):
        nodes = self._model.getCammino(self._view._ddNode.value)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza : {self._view._ddNode.value}"))
        for n in nodes:
            self._view.txt_result.controls.append(ft.Text(n.order_id))
        self._view.update_page()

    def handleRicorsione(self, e):
        bestPath, bestScore = self._model.trovaCammino(self._view._ddNode.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato un cammino che parte da {self._view._ddNode.value} "
                    f"con somma dei pesi uguale a {bestScore}."))

        for v in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{v.order_id}"))
        self._view.update_page()

    def fillDD(self):
        stores = self._model.getStores()
        for store in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(store))

    def fillNodi(self, allNodes):
        self._view._ddNode.options.clear()
        for n in allNodes:
            self._view._ddNode.options.append(ft.dropdown.Option(n.order_id))
