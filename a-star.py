import numpy as np


class CellOfField:
    x = 0
    y = 0
    heuristicApproximation = 0.0
    value = 0.0
    sumValue = 0.0
    parent = None

    def getSumValue(self):
        return self.sumValue

    def setSumValue(self, sumValue):
        self.sumValue = sumValue

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def printCellOfField(self):
        s = 'x=%d y=%d v=%.1f h%.1f s=%.1f   ' % (self.x, self.y, self.value, self.heuristicApproximation, self.sumValue)
        while len(s) < 28:
            s = s + " "
        print(s, end="")

    def printVHS(self):
        s = 'v=%1f h%1f s=%1f   ' % (self.value, self.heuristicApproximation, self.sumValue)
        while len(s) < 21:
            s = s + " "
        print(s, end="")

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def getHeuristicApproximation(self):
        return self.heuristicApproximation

    def setHeuristicApproximation(self, heuristicApproximation):
        self.heuristicApproximation = heuristicApproximation

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value


class Field:
    @staticmethod
    def getStartField(field):
        i = 0
        while i < len(field):
            j = 0
            while j < len(field[0]):
                if (field[i][j] == -1) or (field[i][j] == -2) or (field[i][j] == -3):
                    print("%.1f     " % (field[i][j]), end="", sep="")
                else:
                    print(" %.1f     " % (field[i][j]), end="", sep="")
                j += 1
            print()
            i += 1


class AStar:
    fieldWithParametrs = []
    openList = []
    closeList = []
    xStart = 0
    yStart = 0
    xFinish = 0
    yFinish = 0
    startCell = None
    finishCell = None
    actualCell = None

    def createFieldWithParametrs(self, field):
        i = 0
        while i < len(field):
            self.fieldWithParametrs.insert(i, [])
            j = 0
            while j < len(field[0]):
                if field[i][j] == -2:
                    self.xStart = i
                    self.yStart = j
                if field[i][j] == -3:
                    self.xFinish = i
                    self.yFinish = j
                self.fieldWithParametrs[i].append(CellOfField())
                self.fieldWithParametrs[i][j].setX(i)
                self.fieldWithParametrs[i][j].setY(j)
                self.fieldWithParametrs[i][j].setValue(field[i][j])
                j += 1
            i += 1
        self.startCell = self.fieldWithParametrs[self.xStart][self.yStart]
        self.startCell.setValue(0)
        self.finishCell = self.fieldWithParametrs[self.xFinish][self.yFinish]
        self.actualCell = self.startCell

    def printFieldWithParametrs(self):
        i = 0
        while i < len(self.fieldWithParametrs):
            j = 0
            while j < len(self.fieldWithParametrs[0]):
                self.fieldWithParametrs[i][j].printCellOfField()
                j += 1
            print()
            i += 1

    def printFieldWithParametrsVHS(self):
        i = 0
        while i < len(self.fieldWithParametrs):
            j = 0
            while j < len(self.fieldWithParametrs[0]):
                self.fieldWithParametrs[i][j].printVHS()
                j += 1
            print()
            i += 1

    k = 0

    def goAStar(self):
        while (not ((abs(self.actualCell.getX()) == self.finishCell.getX()) and (
                abs(self.actualCell.getY()) == self.finishCell.getY()))):
            self.k += 1
            if self.k > (len(self.fieldWithParametrs)) * (len(self.fieldWithParametrs[1])) * 100:
                print("Error, way not exist")
                break
            self.closeList.append(self.actualCell)
            i = -1
            while i <= 1:
                j = -1
                while j <= 1:
                    activeCell = self.fieldWithParametrs[self.actualCell.getX() + i][self.actualCell.getY() + j]
                    if (i == 0 and j == 0) or (activeCell.getValue() == -1):
                        j += 1
                        continue
                    if activeCell in self.closeList:
                        j += 1
                        continue
                    if ((i * j == 0) and (activeCell in self.openList and (activeCell.getSumValue() < (
                            activeCell.getValue() + self.actualCell.getSumValue() + activeCell.getHeuristicApproximation() - self.actualCell.getHeuristicApproximation())))):
                        j += 1
                        continue
                    elif (activeCell in self.openList and (activeCell.getSumValue() < (
                            activeCell.getValue() * 1.4 + self.actualCell.getSumValue() + activeCell.getHeuristicApproximation() - self.actualCell.getHeuristicApproximation()))):
                        j += 1
                        continue
                    activeCell.setHeuristicApproximation(max(abs(activeCell.getX() - self.finishCell.getX()),
                                                             abs(activeCell.getY() - self.finishCell.getY())) + min(
                        abs(activeCell.getX() - self.finishCell.getX()),
                        abs(activeCell.getY() - self.finishCell.getY())) * 0.4)
                    activeCell.setParent(self.actualCell)
                    if i * j == 0:
                        activeCell.setSumValue(
                            activeCell.getValue() + self.actualCell.getSumValue() + activeCell.getHeuristicApproximation() - self.actualCell.getHeuristicApproximation())
                    else:
                        activeCell.setSumValue(
                            activeCell.getValue() * 1.4 + self.actualCell.getSumValue() + activeCell.getHeuristicApproximation() - self.actualCell.getHeuristicApproximation())
                    self.openList.append(activeCell)
                    j += 1
                i += 1
            if self.actualCell in self.openList:
                self.openList.remove(self.actualCell)
            minValue = 0
            if len(self.openList) == 0:
                print("Error, way not exist")
                break
            else:
                minValue = self.openList[0].getSumValue()
            self.actualCell = self.openList[0]

            i = 0
            while i < len(self.openList):
                #
                if self.openList[i].getSumValue() < minValue:
                    minValue = self.openList[i].getSumValue()
                    self.actualCell = self.openList[i]
                i += 1

    def getPicture(self):
        s = [[None] * (len(self.fieldWithParametrs[0])) for _ in range(len(self.fieldWithParametrs))]
        i = 0
        while i < len(self.fieldWithParametrs):
            j = 0
            while j < len(self.fieldWithParametrs[0]):
                if self.fieldWithParametrs[i][j].getValue() == -1:
                    s[i][j] = "#######  "
                elif i == self.xStart and j == self.yStart:
                    s[i][j] = "start    "
                else:
                    s[i][j] = str(self.fieldWithParametrs[i][j].getValue()) + "      "
                j += 1
            i += 1
        cellOfField = self.actualCell
        while cellOfField.getParent() is not None:
            s[cellOfField.getX()][cellOfField.getY()] = s[cellOfField.getX()][cellOfField.getY()].replace(" ",
                                                                                                          "") + "====  "
            cellOfField = cellOfField.getParent()
        s[self.finishCell.getX()][self.finishCell.getY()] = "finish   "
        i = 0
        while i < len(self.fieldWithParametrs):
            j = 0
            while j < len(self.fieldWithParametrs[0]):
                print(s[i][j], end="")
                j += 1
            print()
            i += 1

    @staticmethod
    def main():
        height = int((np.random.rand() * 18 + 5))
        wight = int((np.random.rand() * 18 + 5))
        xStart = int((np.random.rand() * (height - 2) + 1))
        yStart = int((np.random.rand() * (wight - 2) + 1))
        xFinish = int((np.random.rand() * (height - 2) + 1))
        yFinish = int((np.random.rand() * (wight - 2) + 1))
        field1 = [[None] * wight for _ in range(height)]
        if xStart == xFinish and yStart == yFinish:
            print("Start is finish")
        i = 0
        while i < height:
            j = 0
            while j < wight:
                if (i == 0) or (i == height - 1) or (j == 0) or (j == wight - 1):
                    field1[i][j] = -1.0
                elif i == xStart and j == yStart:
                    field1[i][j] = -2.0
                elif i == xFinish and j == yFinish:
                    field1[i][j] = -3.0
                else:
                    k = int((np.random.rand() * 10 if np.random.rand() * 14 < 10 else -1))
                    # int k = (int)(Math.random() * 15 < 10 ? Math.random()*10 : -1);
                    if k == 0:
                        k = 1
                    field1[i][j] = float(k)
                j += 1
            i += 1
        Field.getStartField(field1)
        aStar = AStar()
        aStar.createFieldWithParametrs(field1)
        aStar.goAStar()
        aStar.getPicture()


if __name__ == "__main__":
    AStar.main()
