import sys
import calendar
import math
import datetime
import requests
from scipy.stats import norm
from bs4 import BeautifulSoup

if sys.version[0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk
    from tkinter import ttk

class Calendar:
    def __init__(self, parent, values):
        self.values = values
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.wid = []
        self.day_selected = 1
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''
        
        self.setup(self.year, self.month)
        
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            #w.destroy()
            self.wid.remove(w)
    
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)

    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
        
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)
        
    def selection(self, day, name):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name
        
        #data
        self.values['day_selected'] = day
        self.values['month_selected'] = self.month
        self.values['year_selected'] = self.year
        self.values['day_name'] = name
        self.values['month_name'] = calendar.month_name[self.month_selected]
        
        self.clear()
        self.setup(self.year, self.month)
        
    def setup(self, y, m):
        left = tk.Button(self.parent, text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)
        
        header = tk.Label(self.parent, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)
        
        right = tk.Button(self.parent, text='>', command=self.go_next)
        self.wid.append(right)
        right.grid(row=0, column=5)
        
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3])
            self.wid.append(t)
            t.grid(row=1, column=num)
        
        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    #print(calendar.day_name[day])
                    b = ttk.Button(self.parent, width=3, text=day, command=lambda day=day:self.selection(day, calendar.day_name[(day-1) % 7]))
                    self.wid.append(b)
                    b.grid(row=w, column=d)
                    
        sel = tk.Label(self.parent, height=2, text='{} {} {} {}'.format(
            self.day_name, calendar.month_name[self.month_selected], self.day_selected, self.year_selected))
        self.wid.append(sel)
        sel.grid(row=8, column=0, columnspan=7)
        
        ok = ttk.Button(self.parent, width=5, text='OK', command=self.kill_and_save)
        self.wid.append(ok)
        ok.grid(row=9, column=2, columnspan=3, pady=10)
        
    def kill_and_save(self):
        self.parent.destroy()


if __name__ == '__main__':
    class Control:
        def __init__(self, parent):
            self.parent = parent
            
            self.parent.geometry('550x600')     # 視窗大小
            self.parent.title('B-S Model')      # 視窗title
            self.parent.resizable(0,0)          # 視窗不可調整大小
            
            self.D1 = tk.Label(self.parent, text='Please enter the required parameters for calculating B-S Model').place(x=30, y=30)
            self.D2 = tk.Label(self.parent, text='Select model: ').place(x=30, y=70)            

            self.comboVar = tk.StringVar()
            self.comboChosen = ttk.Combobox(self.parent, width=25, textvariable = self.comboVar, state='readonly')
            self.comboChosen.bind("<<ComboboxSelected>>", self.ComboboxEvent)
            self.comboChosen['values']=('Black-Scholes Model', 'Merton Model', 'Future', 'TAIFEX Future')
            self.comboChosen.current(0)
            self.comboChosen.place(x=125, y=70)        
            
            tk.Label(self.parent, text='Select Date: ').place(x=35, y=105)
            self.DateVar = tk.StringVar()
            self.Ent_Date = tk.Entry(self.parent, width=15 ,textvariable = self.DateVar, state = "disabled")        # 日期 Entry
            self.Ent_Date.place(x=125, y=105)   

            # 日期按鈕
            self.DateButton = ttk.Button(self.parent, text='Select Date',command=self.popup)
            self.DateButton.place(x=250, y=102)  

            # GET按鈕
            self.GetButton = ttk.Button(self.parent, text='GET',command=self.getinfo)
            self.GetButton.place(x=350, y=102)

            # 預設日期按鈕 & GET按鈕 Disable
            self.GetButton.configure(state='disabled')      # Get Button Disable
            self.DateButton.configure(state='disabled')     # Date Button disable

            #ttk.Button(self.parent, text='Show Selected',command=self.print_selected_date).place(x=450, y=102)

            # 顯示參數名稱
            self.ypos = 150
            self.A1 = tk.Label(self.parent, text='S : ').place(x=30, y= self.ypos) 
            self.A2 = tk.Label(self.parent, text='K : ').place(x=30, y= self.ypos+30) 
            self.A3 = tk.Label(self.parent, text='r : ').place(x=30, y= self.ypos+60)
            self.A4 = tk.Label(self.parent, text='q : ').place(x=30, y= self.ypos+90)            
            self.A5 = tk.Label(self.parent, text='t : ').place(x=30, y= self.ypos+120)    
            self.A6 = tk.Label(self.parent, text='v : ').place(x=30, y= self.ypos+150)

            self.SS = tk.StringVar()
            self.KK = tk.StringVar()
            self.rr = tk.StringVar()
            self.qq = tk.StringVar()            
            self.tt = tk.StringVar()
            self.vv = tk.StringVar()
            
            # 參數輸入
            self.Ent_S = tk.Entry(self.parent, textvariable = self.SS)                       # 股價
            self.Ent_K = tk.Entry(self.parent, textvariable = self.KK)                       # 履約價
            self.Ent_r = tk.Entry(self.parent, textvariable = self.rr)                       # 無風險利率
            self.Ent_q = tk.Entry(self.parent, textvariable = self.qq, state = "disabled")   # 股息率            
            self.Ent_t = tk.Entry(self.parent, textvariable = self.tt)                       # 到期時間
            self.Ent_v = tk.Entry(self.parent, textvariable = self.vv)                       # 波動率
            self.Ent_S.place(x=70, y=self.ypos)
            self.Ent_K.place(x=70, y=self.ypos+30)
            self.Ent_r.place(x=70, y=self.ypos+60)
            self.Ent_q.place(x=70, y=self.ypos+90)            
            self.Ent_t.place(x=70, y=self.ypos+120)
            self.Ent_v.place(x=70, y=self.ypos+150)

            # 履約價combobox
            self.Kcombo = ttk.Combobox(self.parent, width=18, textvariable = self.KK, state='readonly')
            self.Kcombo.bind("<<ComboboxSelected>>", self.KComboEvent)
            self.Kcombo['values']=('9800', '9900', '10000', '10100', '10200', '10300', '10400', '10500', '10600', '10700', '10800', '10900', '11000', '11100','11200', '11300')
            self.Kcombo.current(0)
            #self.Kcombo.place(x=70, y=ypos+30)    
            
            # 說明
            tk.Label(self.parent, text='S: initial stock price').place(x=235, y=self.ypos) 
            tk.Label(self.parent, text='K: Strike price').place(x=235, y=self.ypos+30) 
            tk.Label(self.parent, text='r: annual risk-free interest rate!').place(x=235, y=self.ypos+60) 
            tk.Label(self.parent, text='q: annual dividend yield').place(x=235, y=self.ypos+90)             
            tk.Label(self.parent, text='t: time to maturity (in year)').place(x=235, y=self.ypos+120)
            tk.Label(self.parent, text='v: annual volatility of stock return rate').place(x=235, y=self.ypos+150) 

            # 清除Entry資料
            self.clearEntry()

            # "計算" 按鈕
            self.BTN = ttk.Button(self.parent, text='Calculate', command = self.Cal_CallPut)
            self.BTN.place(x=70, y=340)

            # 顯示Label
            self.MarketInfoLabel = ttk.Label(self.parent, text='Market Information: ')
            #self.MarketInfoLabel.place(x= 35, y= 410) 
            self.CalculateLabel = ttk.Label(self.parent, text='Calculated Information: ')
            self.CalculateLabel.place(x=285, y=410)

            self.TXFCallLabel_A = ttk.Label(self.parent, text='TXF Call: ')
            #self.TXFCallLabel_A.place(x= 45, y= 440) 
            self.TXFPutLabel_A = ttk.Label(self.parent, text='TXF Put: ')
            #self.TXFPutLabel_A.place(x= 45, y= 470) 

            self.CallLabel = ttk.Label(self.parent, text='Call Price: ')
            self.CallLabel.place(x=285, y=440)

            self.PutLabel = ttk.Label(self.parent, text='Put Price: ')
            self.PutLabel.place(x=285, y=470)


            self.TXFCallText = tk.StringVar()
            self.TXFCallLabel_B = ttk.Label(self.parent, textvariable = self.TXFCallText)
            #self.TXFCallLabel_B.place(x= 105, y= 440) 
            self.TXFCallText.set("Call Price")

            self.TXFPutText = tk.StringVar()
            self.TXFPutLabel_B = ttk.Label(self.parent, textvariable = self.TXFPutText)
            #self.TXFPutLabel_B.place(x= 105, y= 470) 
            self.TXFPutText.set("Put Price")

            self.CallPriceText = tk.StringVar()
            ttk.Label(self.parent, textvariable = self.CallPriceText).place(x= 360, y= 440) 
            self.CallPriceText.set("CALL PRICE")

            self.PutPriceText = tk.StringVar()
            ttk.Label(self.parent, textvariable = self.PutPriceText).place(x=360, y= 470) 
            self.PutPriceText.set("PUT PRICE")

            self.data = {}
            

        def Cal_CallPut(self):      # 計算Call & Put
            item = self.comboChosen.current()

            if item == 0:       # B-S model
                pass
            elif item == 1:     # Merton
                S = float(self.SS.get())
                K = float(self.KK.get())
                r = float(self.rr.get())
                t = float(self.tt.get())
                v = float(self.vv.get())
                q = float(self.qq.get())
                #公式修改
                d1 = ((math.log(S/K))+(r-q+0.5*(v**2))*t)/(v*(t**0.5))
                d2 = d1-v*(t**0.5)
                Nd1 = norm.cdf(d1)
                Nd2 = norm.cdf(d2)       
                Nd1m = norm.cdf(-d1)
                Nd2m = norm.cdf(-d2)
                Callprice=S*Nd1-K*(math.exp(-r*t))*Nd2
                Putprice=K*(math.exp(-r*t))*Nd2m-S*Nd1m

                self.CallPriceText.set(round(Callprice, 2))
                self.PutPriceText.set(round(Putprice, 2))

            elif item == 2:
                pass
            elif item == 3:
                S = float(self.SS.get())
                K = float(self.KK.get())
                r = float(self.rr.get())
                t = float(self.tt.get())
                v = float(self.vv.get())
                d1 = ((math.log(S/K))+(r+0.5*(v**2))*t)/(v*(t**0.5))
                d2 = d1-v*(t**0.5)
                Nd1 = norm.cdf(d1)
                Nd2 = norm.cdf(d2)       
                Nd1m = norm.cdf(-d1)
                Nd2m = norm.cdf(-d2)
                Callprice=S*Nd1-K*(math.exp(-r*t))*Nd2
                Putprice=K*(math.exp(-r*t))*Nd2m-S*Nd1m

                self.CallPriceText.set(round(Callprice, 2))
                self.PutPriceText.set(round(Putprice, 2))

        def ComboboxEvent(self, event):
            item = self.comboChosen.current()
            #self.PutPriceText.set(self.comboChosen.get())

            if item == 0:
                print("Black-Scholes Model")
                self.Ent_q.configure(state='disabled')          # disable q
                self.Ent_Date.configure(state='disabled')       # disable date
                self.GetButton.configure(state='disabled')      # Get Button Disable
                self.DateButton.configure(state='disabled')     # Date Button disable
                self.Ent_K.place(x=70, y=self.ypos+30)
                self.Kcombo.place_forget()


                # 左邊顯示disable
                self.disableMarketDisplay()

                # 清除Entry資料
                self.clearEntry()

            elif item == 1:
                print("Merton")
                self.Ent_q.configure(state='normal')        # enable q
                self.Ent_Date.configure(state='disabled')   # disable date
                self.GetButton.configure(state='disabled')      # Get Button Disable
                self.DateButton.configure(state='disabled')     # Date Button disable
                self.Ent_K.place(x=70, y=self.ypos+30)
                self.Kcombo.place_forget()

                # 左邊顯示disable
                self.disableMarketDisplay()

                # 清除Entry資料
                self.clearEntry()

            elif item == 2:
                print("Future")
                self.Ent_q.configure(state='disabled')      # disable q
                self.Ent_Date.configure(state='disabled')   # disable date
                self.GetButton.configure(state='disabled')      # Get Button Disable
                self.DateButton.configure(state='disabled')     # Date Button disable
                self.Ent_K.place(x=70, y=self.ypos+30)
                self.Kcombo.place_forget()

                # 左邊顯示disable
                self.disableMarketDisplay()

                # 清除Entry資料
                self.clearEntry()

            elif item == 3:
                print("TAIFEX Future")
                self.Ent_q.configure(state='disabled')      # disable q
                self.Ent_Date.configure(state='disabled')     # enable date
                self.GetButton.configure(state='normal')      # Get Button Enable
                self.DateButton.configure(state='normal')     # Date Button Enable
                self.Ent_K.place_forget()
                self.Kcombo.place(x=70, y=self.ypos+30)

                # 左邊顯示enable
                #self.enableMarketDisplay()

                # 清除Entry資料
                self.clearEntry()


        def KComboEvent(self, event):
            '''
            # 選擇權每日收盤行情
            self.url = ('http://www.taifex.com.tw/chinese/3/3_2_1.asp?qtype=2&commodity_id=TXO&commodity_id2=&commodity_name=%E8%87%BA%E6%8C%87%E9%81%B8%E6%93%87%E6%AC%8A%28TXO%29&goday=&dateaddcnt=0&DATA_DATE_Y={0}&DATA_DATE_M={1}&DATA_DATE_D={2}&syear={0}&smonth={1}&sday={2}&market_code=0&datestart={0}%2F{1}%2F{2}&MarketCode=0&commodity_idt=TXO&commodity_id2t=')
            res = requests.get(self.url.format(self.data['year_selected'], self.data['month_selected'], self.data['day_selected']))
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "lxml")
            tableF = soup.select('.clearfix')
            print(tableF)
            #closeF = tableF.select('tr')[1].select('td')[5].text    # 取得期貨收盤價的表格資訊
            #self.SS.set(closeF)       
            '''

            item = self.Kcombo.get()
            print(item)

        def clearEntry(self):
            # 清除Entry資料
            self.Ent_S.delete(0, 'end')
            self.Ent_K.delete(0, 'end')
            self.Ent_r.delete(0, 'end')
            self.Ent_t.delete(0, 'end')
            self.Ent_v.delete(0, 'end')
        
        def disableMarketDisplay(self):
            self.MarketInfoLabel.place_forget()
            self.TXFCallLabel_A.place_forget()
            self.TXFPutLabel_A.place_forget()    
            self.TXFCallLabel_B.place_forget()
            self.TXFPutLabel_B.place_forget()

        def enableMarketDisplay(self):
            self.MarketInfoLabel.place(x= 45, y= 410) 
            self.TXFCallLabel_A.place(x= 45, y= 440) 
            self.TXFPutLabel_A.place(x= 45, y= 470) 
            self.TXFCallLabel_B.place(x= 105, y= 440) 
            self.TXFPutLabel_B.place(x= 105, y= 470) 

        def getFuturePrice(self):
            pass
            #url = ('www.taifex.com.tw/chinese/3/3_1_1.asp?qtype=2&commodity_id=TX&commodity_id2=&market_code=0&goday=&dateaddcnt=0&DATA_DATE_Y={0}&DATA_DATE_M={1}&DATA_DATE_D={2}&syear={0}&smonth={1}&sday={2}&datestart={0}%2F{1}%2F{2}&MarketCode=0&commodity_idt=TX&commodity_id2t=&commodity_id2t2=')

        def popup(self):
            child = tk.Toplevel()
            cal = Calendar(child, self.data)

        def getinfo(self):      # 取得網路資料
            # 顯示日期
            DateStr = str(self.data['year_selected'])+"-"+str(self.data['month_selected'])+"-"+str(self.data['day_selected'])
            self.DateVar.set(DateStr)

            # 期交所每日收盤行情
            self.urlA = ('https://www.taifex.com.tw/chinese/3/3_1_1.asp?qtype=2&commodity_id=TX&commodity_id2=&market_code=0&goday=&dateaddcnt=0&DATA_DATE_Y={0}&DATA_DATE_M={1}&DATA_DATE_D={2}&syear={0}&smonth={1}&sday={2}&datestart={0}%2F{1}%2F{2}&MarketCode=0&commodity_idt=TX&commodity_id2t=&commodity_id2t2=')
            
            # 台灣銀行新台幣存放款利率
            self.urlB = ('http://rate.bot.com.tw/twd/{0}-{1}-{2}')

            # 期交所波動率指數
            self.urlC = ('http://info512.taifex.com.tw/Future/VIXQuote_Norl.aspx')          # 現在的波動率網站
            #self.urlC = ('https://www.taifex.com.tw/chinese/7/log2data/{0}{1}new.txt')     # 過去30日的波動率網站
            
            res = requests.get(self.urlA.format(self.data['year_selected'], self.data['month_selected'], self.data['day_selected']))
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "lxml")
            tableF = soup.select('.table_f')[0]
            closeF = tableF.select('tr')[1].select('td')[5].text    # 取得期貨收盤價的表格資訊
            self.SS.set(closeF)                                     # 期貨收盤價寫入SS

            res = requests.get(self.urlB.format(self.data['year_selected'], self.data['month_selected'], self.data['day_selected']))
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "lxml")
            tableF = soup.select('table')[0]
            valueR = float(tableF.select('tr')[3].select('td')[4].text) * 0.01            
            self.rr.set(valueR)               # 定期存款利率寫入rr

            # 取得波動率數據 (新)
            res = requests.get(self.urlC)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "lxml")
            valueV = soup.select('.custDataGridRow')[1].select('td')[1].text
            self.vv.set(round(float(valueV)*0.01, 5))

            # 取得波動率 (過去三十日)
            '''
            res = requests.get(self.urlC.format(self.data['year_selected'], self.data['month_selected']-1))
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "lxml")
            valueV = soup.select('body')[0].text
            arrV = valueV.split()
            varTotal = 0.0
            varCnt = 0
            varAvg = 0      # 平均
            for item in arrV:
                if float(item) < 1000:
                    varTotal = varTotal + float(item)
                    varCnt = varCnt + 1
                    varAvg = varTotal / varCnt
                    
            self.vv.set(round(varAvg * 0.01, 2))
            '''
            #print(valueV)
            
        def print_selected_date(self):
            print(self.data) 
            #print(self.data['day_selected'])
            #print(self.data['month_selected'])
            #print(self.data['year_selected'])

    root = tk.Tk()
    app = Control(root)
    root.mainloop()