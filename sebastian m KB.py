
def turun_mas(c, cmin, cmax):
    return (cmax-c)/(cmax-cmin)

def naik_mas(c, cmin, cmax):
    return(c-cmin)/(cmax-cmin)

class Permintaan():
    minimal = 2049
    maximal = 7493
    median = 4861

    def down(self, c):
        if c >= self.median:
            return 0
        elif c <= self.minimal:
            return 1
        else :
            return turun_mas(c, self.minimal, self.median)
    
    def up(self, c):
        if c >= self.maximal:
            return 1
        elif c <= self.median:
            return 0
        else :
            return naik_mas(c, self.median  , self.maximal)
    
    def consistent(self, c):
        if c >= self.maximal or c <= self.minimal:
            return 0
        elif self.minimal < c < self.median:
            return naik_mas(c, self.minimal, self.median)
        elif self.median < c < self.maximal:
            return turun_mas(c, self.median, self.maximal)
        else :
            return 1

class Persediaan():
    minimal = 550
    maximal = 1285

    def sedikit(self, s):
        if s >= self.maximal:
            return 0
        elif s <= self.minimal:
            return 1
        else :
            return turun_mas(s, self.minimal, self.maximal)
    
    def banyak(self, s):
        if s >= self.maximal:
            return 1
        elif s <= self.minimal:
            return 0
        else :
            return naik_mas(s, self.minimal, self.maximal)

class Produksi():
    minimal = 3719
    maximal = 6769
    permintaan = 0
    persediaan = 0

    def _kurang(self, t):
        return self.maximal - t*(self.maximal - self.minimal)

    def _tambah(self, t):
        return t*(self.maximal - self.minimal) + self.minimal

    def _inferensi(self, pmt=Permintaan(), psd=Persediaan()):
        result = []
        q1 = min(pmt.down(self.permintaan), psd.banyak(self.persediaan))
        t1 = self._kurang(q1)
        result.append((q1, t1))
        q2 = min(pmt.down(self.permintaan), psd.sedikit(self.persediaan))
        t2 = self._kurang(q2)
        result.append((q2, t2))
        q3 = min(pmt.up(self.permintaan), psd.banyak(self.persediaan))
        t3 = self._tambah(q3)
        result.append((q3, t3))
        q4 = min(pmt.up(self.permintaan), psd.sedikit(self.persediaan))
        t4 = self._kurang(q4)
        result.append((q4, t4))
        q5 = min(pmt.consistent(self.permintaan), psd.sedikit(self.persediaan))
        t5 = self._tambah(q5)
        result.append((q5, t5))
        q6 = min(pmt.consistent(self.permintaan), psd.sedikit(self.persediaan))
        t6 = self._kurang(q6)
        result.append((q6, t6))
        return result

    def defuzifikasi(self, data_inferensi=[]):
        data_inferensi = data_inferensi if data_inferensi else self._inferensi()
        res_q_w = 0
        res_q = 0
        for data in data_inferensi:
            res_q_w += data[0] * data[1]
            res_q += data[0]
        return res_q_w/res_q