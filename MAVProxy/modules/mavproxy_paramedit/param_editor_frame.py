#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.1 on Wed May  8 16:56:24 2019
#
import wx
import wx.grid
import os
import sys
import time
import math

from MAVProxy.modules.lib import multiproc
from MAVProxy.modules.mavproxy_paramedit import checklisteditor as cle
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.mavproxy_paramedit import ph_event
ParamEditorEvent = ph_event.ParamEditorEvent

# begin wxGlade: extracode
# end wxGlade

# define column names via "enums":
PE_PARAM = 0
PE_VALUE = 1
PE_UNITS = 3
PE_OPTION = 2
PE_DESC = 4


class ParamEditorFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ParamEditor.__init__
        wx.Frame.__init__(self, *args, **kwds)
        self.read_file = wx.Button(self, wx.ID_ANY, ("Read From File"))
        self.write_file = wx.Button(self, wx.ID_ANY, ("Write To File"))
        self.reset_params = wx.Button(self, wx.ID_ANY, ("Reset To Default"))
        self.read_params = wx.Button(self, wx.ID_ANY, ("Discard Changes"))
        self.fetch_params = wx.Button(self, wx.ID_ANY, ("Fetch all"))
        self.write_params = wx.Button(self, wx.ID_ANY, ("Write"))
        self.search_key = wx.TextCtrl(self, wx.ID_ANY, "")
        self.display_list = wx.grid.Grid(self, wx.ID_ANY, size=(1, 1))
        self.search_key.SetHint("Search")
        self.__set_properties()
        self.__do_layout()
        self.param_received = {}
        self.modified_param = {}
        self.requires_redraw = False
        self.last_grid_update = time.time()
        self.htree = {}

        self.Bind(wx.EVT_BUTTON, self.Read_File, self.read_file)
        self.Bind(wx.EVT_BUTTON, self.Write_File, self.write_file)
        self.Bind(wx.EVT_BUTTON, self.reset_param, self.reset_params)
        self.Bind(wx.EVT_BUTTON, self.read_param, self.read_params)
        self.Bind(wx.EVT_BUTTON, self.fetch_param, self.fetch_params)
        self.Bind(wx.EVT_BUTTON, self.write_param, self.write_params)
        self.Bind(wx.EVT_TEXT, self.key_change, self.search_key)
        if float(str(wx.__version__).split('.')[0]) < 4.0:
            self.Bind(wx.grid.EVT_GRID_CMD_CELL_CHANGE, self.ParamChanged,
                      self.display_list)
        else:
            self.Bind(wx.grid.EVT_GRID_CMD_CELL_CHANGING, self.ParamChanged,
                      self.display_list)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onSelect, self.display_list)
        self.Bind(wx.grid.EVT_GRID_COL_SIZE, self.ColChanged, self.display_list)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.grid.EVT_GRID_EDITOR_CREATED, self.EditorCreated, self.display_list)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.time_to_process_gui_events, self.timer)
        self.timer.Start(200)
        renderer = wx.grid.GridCellAutoWrapStringRenderer()
        self.ro_attr = wx.grid.GridCellAttr()
        self.ro_attr.SetReadOnly(True)
        self.ce_attr = wx.grid.GridCellAttr()
        self.ce_attr.SetAlignment(hAlign=wx.ALIGN_CENTER, vAlign=wx.ALIGN_CENTER)
        self.display_list.SetColAttr(PE_PARAM, self.ro_attr)
        self.display_list.SetColAttr(PE_UNITS, self.ro_attr)
        self.display_list.SetColAttr(PE_DESC, self.ro_attr)
        self.display_list.SetColAttr(PE_VALUE, self.ce_attr)
        self.display_list.SetRowLabelSize(0)
        self.display_list.SetDefaultRenderer(renderer)

        self.xml_filepath = None
        self.last_param_file_path = ""
        font = wx.Font(pointSize=10, family=wx.DEFAULT,
                       style=wx.NORMAL, weight=wx.NORMAL,
                       faceName='Consolas')
        self.dc = wx.ScreenDC()
        self.dc.SetFont(font)

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ParamEditor.__set_properties
        self.SetTitle(("Parameter Editor"))
        self.SetSize((800, 550))
        self.display_list.CreateGrid(10, 5)
        self.display_list.SetColLabelValue(PE_PARAM, ("Param"))
        self.display_list.SetColLabelValue(PE_VALUE, ("Value"))
        self.display_list.SetColLabelValue(PE_UNITS, ("Units"))
        self.display_list.SetColLabelValue(PE_OPTION, ("Selections"))
        self.display_list.SetColLabelValue(PE_DESC, ("Description"))
        self.display_list.SetColSize(PE_PARAM, 200)
        self.display_list.SetColSize(PE_UNITS, 100)
        self.display_list.SetColSize(PE_VALUE, 100)
        self.display_list.SetColSize(PE_DESC, 250)
        self.display_list.SetColSize(PE_OPTION, 150)
        self.display_list.SetColFormatFloat(PE_VALUE, precision=4)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ParamEditor.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add((10, 10), 0, 0, 0)
        sizer_6.Add((10, 10), 0, 0, 0)
        sizer_6.Add(self.read_file, 0, wx.ALIGN_CENTER, 0)
        sizer_6.Add((10, 10), 0, 0, 0)
        sizer_6.Add(self.write_file, 0, wx.ALIGN_CENTER, 0)
        sizer_6.Add((10, 10), 0, 0, 0)
        sizer_6.Add(self.fetch_params, 0, wx.ALIGN_CENTER, 0)
        sizer_6.Add((10, 10), 0, 0, 0)
        sizer_6.Add(self.reset_params, 0, wx.ALIGN_CENTER, 0)
        sizer_6.Add((10, 10), 0, 0, 0)
        sizer_3.Add(sizer_6, 0, 0, 0)
        sizer_3.Add((10, 10), 0, 0, 0)
        sizer_5.Add((10, 10), 0, 0, 0)
        sizer_5.Add(self.read_params, 0, 0, 0)
        sizer_5.Add((10, 10), 0, 0, 0)
        sizer_5.Add(self.write_params, 0, 0, 0)
        sizer_5.Add((10, 10), 0, 0, 0)
        sizer_5.Add(self.search_key, 0, 0, 0)
        sizer_5.Add((10, 10), 0, 0, 0)
        sizer_3.Add(sizer_5, 0, 0, 0)
        sizer_2.Add(sizer_3, 0, 0, 0)
        sizer_2.Add((10, 10), 0, 0, 0)
        sizer_2.Add(self.display_list, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND,  0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def redirect_err(self, moddebug):
        if moddebug < 3:
            sys.stderr.flush()
            err = open(os.devnull, 'a+', 0)
            os.dup2(err.fileno(), sys.stderr.fileno())

    def OnCloseWindow(self, event):
        self.event_queue_lock.acquire()
        self.event_queue.put(ParamEditorEvent(ph_event.PEE_TIME_TO_QUIT))
        self.event_queue_lock.release()
        event.Skip()

    def onSelect(self, event):
        if self.display_list.GetNumberRows() == 0:
            return
        self.oldval = self.display_list.GetCellValue(event.Row, PE_VALUE)
        if event.Col == PE_OPTION:
            wx.CallAfter(self.display_list.EnableCellEditControl)
        event.Skip()

    def set_param_init(self, params, vehicle):
        self.vehicle_name = vehicle
        self.param_received = params
        self.get_vehicle_type(vehicle)
        self.redraw_grid(params)

    def EditorCreated(self, evt):
        if evt.Col == PE_OPTION:
            self.combo = evt.GetControl()
            self.row = evt.Row
            self.combo.Bind(wx.EVT_CHECKLISTBOX, self.checklist)
            self.combo.Bind(wx.EVT_COMBOBOX, self.combobox)
            self.combo.Bind(wx.EVT_SPINCTRLDOUBLE, self.spinctrl)
        evt.Skip()

    def spinctrl(self, event):
        try:
            self.display_list.SetCellValue(self.row, PE_VALUE, str(self.combo.GetValue()))
        except Exception as e:
            pass
        event.Skip()

    def combobox(self, event):
        try:
            self.display_list.SetCellValue(self.row, PE_VALUE, str(self.combo.GetStringSelection()).split(':')[0])
        except Exception as e:
            pass
        event.Skip()

    def checklist(self, event):
        try:
            s = 0
            for i in self.combo.GetChecked():
                s = s + int(math.pow(2, i))
            self.display_list.SetCellValue(self.row, PE_VALUE, str(s))
        except Exception as e:
            pass
        event.Skip()

    def set_event_queue(self, q):
        self.event_queue = q

    def set_event_queue_lock(self, l):
        self.event_queue_lock = l

    def set_gui_event_queue(self, q):
        self.gui_event_queue = q

    def set_gui_event_queue_lock(self, l):
        self.gui_event_queue_lock = l

    def set_close_window_semaphore(self, sem):
        self.close_window_semaphore = sem

    def time_to_process_gui_events(self, evt):
        event_processed = False
        self.gui_event_queue_lock.acquire()
        while self.gui_event_queue.qsize() > 0:
            event_processed = True
            try:
                event = self.gui_event_queue.get(block=False)
                self.process_gui_event(event)
            except Exception as e:
                pass

        self.gui_event_queue_lock.release()

        if self.requires_redraw and ((time.time() - self.last_grid_update) > 0.1):
            self.redraw_grid(self.param_received)
            self.requires_redraw = False

        if (event_processed):
            # redraw window to apply changes
            self.Refresh()
            self.Update()

    def ColChanged(self, event):
        for row in range(self.display_list.GetNumberRows()):
            self.set_row_size(row)

    def process_gui_event(self, event):
        if event.get_type() == ph_event.PEGE_READ_PARAM:
            self.param_received.clear()
            self.param_received = event.get_arg("param")
            if self.vehicle_name is None or len(self.htree) == 0:
                self.get_vehicle_type(event.get_arg("vehicle"))
            self.redraw_grid(self.param_received)
        elif event.get_type() == ph_event.PEGE_WRITE_SUCC:
            if event.get_arg("paramid") in self.param_received.keys():
                if event.get_arg("paramid") in self.modified_param.keys():
                    del self.modified_param[event.get_arg("paramid")]
                for row in range(self.display_list.GetNumberRows()):
                    if self.display_list.GetCellValue(row, PE_PARAM) == event.get_arg("paramid"):
                        self.display_list.SetCellValue(row, PE_VALUE, str(round(event.get_arg("paramvalue"), 4)))
                        self.display_list.SetCellBackgroundColour(row, PE_VALUE,
                                                                  wx.Colour(255, 255, 255))
            else:
                self.param_received[event.get_arg("paramid")] = event.get_arg("paramvalue")
                self.requires_redraw = True

    def redraw_grid(self, datalist):
        self.display_list.ClearGrid()
        if (self.display_list.GetNumberRows() > 0):
            self.display_list.DeleteRows(0, self.display_list.GetNumberRows())
        self.display_list.AppendRows(len(datalist))
        row = 0
        for paramname, paramvalue in sorted(datalist.items()):
            self.add_new_row(row, paramname, paramvalue)
            row = row + 1
        self.display_list.ForceRefresh()
        self.last_grid_update = time.time()

    def add_new_row(self, row, name, pvalue):
        self.display_list.SetCellValue(row, PE_PARAM, str(name))
        self.display_list.SetCellValue(row, PE_VALUE, str(round(pvalue, 4)))
        unit, option, desc = self.getinfo(name)
        self.display_list.SetCellValue(row, PE_UNITS, unit)
        self.display_list.SetCellValue(row, PE_DESC, desc)
        if (name in [keys for keys, va in self.modified_param.items()]):
            self.display_list.SetCellBackgroundColour(row, PE_VALUE,
                                                      wx.Colour(152, 251, 152))
        self.set_row_size(row)
        try:
            for f in self.htree[name].field:
                if f.get('name') == "Bitmask":
                    bits = str(f).split(',')
                    self.display_list.SetCellEditor(row, PE_OPTION, cle.GridCheckListEditor(bits, PE_VALUE, pvalue))
                    val = ""
                    binary = bin(int(pvalue))[2:]
                    for i in [(len(binary)-ones-1) for ones in range(len(binary)) if binary[ones] == '1']:
                        val = val + str(bits[i]) + "\n"
                    self.display_list.SetCellValue(row, PE_OPTION, str(val))
                    self.set_row_size(row, 25*len(bits))
                    return
        except Exception as e:
            pass
        try:
            if self.htree[name].values is not None:
                v = self.htree[name].findall('values')[0].getchildren()
                for i in range(len(v)):
                    if float(v[i].get('code')) == pvalue:
                        selected = str(v[i].get('code'))+":"+str(v[i])
                        sel_ind = i
                    v[i] = str(v[i].get('code'))+":"+str(v[i])
                self.display_list.SetCellEditor(row, PE_OPTION, cle.GridDropListEditor(v, PE_VALUE, sel_ind))
                self.display_list.SetCellValue(row, PE_OPTION, str(selected))
                return
        except Exception as e:
            pass
        Range = {}
        try:
            for f in self.htree[name].field:
                if f.get('name') == "Increment":
                    Range['Increment'] = float(f)
                if f.get('name') == "Range":
                    Range['Min'] = float(str(f).split(' ')[0])
                    Range['Max'] = float(str(f).split(' ')[1])
        except Exception as e:
            pass
        if len(Range) > 1:
            if len(Range) == 2:
                Range['Increment'] = (float(Range['Max'])-float(Range['Min']))/10
            self.display_list.SetCellEditor(row, PE_OPTION, cle.GridScrollEditor(Range, PE_VALUE, pvalue))
            self.display_list.SetCellValue(row, PE_OPTION, str(round(pvalue, 4)))
            return
        self.display_list.SetCellValue(row, PE_OPTION, option)

    def set_row_size(self, row, size=0):
        w, h = self.dc.GetTextExtent(self.display_list.GetCellValue(row, PE_DESC))
        self.display_list.SetRowSize(row, max(25*int(w/self.display_list.GetColSize(PE_DESC)+3), size))

    def getinfo(self, name):
        # Provide data derived from XML
        unit = ""
        option = ""
        try:
            desc = str(self.htree[name].get('humanName')) + "\n\n" + str(self.htree[name].get('documentation'))
        except Exception as e:
            desc = str(e)
        try:
            for f in self.htree[name].field:
                if f.get('name') == "Units":
                    unit = str(f)
        except Exception as e:
            unit = ""
        try:
            for f in self.htree[name].field:
                if f.get('name') == "Range":
                    option = "Range:"+str(f)
        except Exception as e:
            option = ""
        return(unit, option, desc)

    def Read_File(self, event):  # wxGlade: ParamEditor.<event_handler>
        fd = wx.FileDialog(self, "Open Parameter File", os.getcwd(), "",
                           "*.parm|*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if (fd.ShowModal() == wx.ID_CANCEL):
            return  # user changed their mind...

        self.event_queue_lock.acquire()
        self.event_queue.put(ParamEditorEvent(ph_event.PEE_LOAD_FILE,
                                              path=fd.GetPath()))
        self.event_queue_lock.release()

        self.last_param_file_path = fd.GetPath()

        event.Skip()

    def Write_File(self, event):  # wxGlade: ParamEditor.<event_handler>
        fd = wx.FileDialog(self, "Save Parameter File", os.getcwd(),
                           os.path.basename(self.last_param_file_path),
                           "*.parm|*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if (fd.ShowModal() == wx.ID_CANCEL):
            return  # user change their mind...

        self.event_queue_lock.acquire()
        self.event_queue.put(ParamEditorEvent(ph_event.PEE_SAVE_FILE,
                                              path=fd.GetPath()))
        self.event_queue_lock.release()

        self.last_param_file_path = fd.GetPath()

        event.Skip()

    def format_params(self):
        self.event_queue_lock.acquire()
        self.event_queue.put(ParamEditorEvent(ph_event.PEE_RESET))
        self.event_queue_lock.release()

    def fetch_param(self, event):
        self.event_queue_lock.acquire()
        self.event_queue.put(ParamEditorEvent(ph_event.PEE_FETCH))
        self.event_queue_lock.release()

    def reset_param(self, event):  # wxGlade: ParamEditor.<event_handler>
        dlg = wx.MessageDialog(self, "Are you sure you want to reset all parameters to default values?", "Reset to default", wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.format_params()
        event.Skip()

    def select_xml(self):
        # Expose this function to set XML file path
        fd = wx.FileDialog(self, "Select XML File", os.getcwd(),
                           os.path.basename(self.last_param_file_path),
                           "*.xml|*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if (fd.ShowModal() == wx.ID_CANCEL):
            return  # user change their mind...

        self.xml_filepath = fd.GetPath()
        self.param_help_tree()

    def read_param(self, event):  # wxGlade: ParamEditor.<event_handler>
        self.event_queue_lock.acquire()
        self.event_queue.put(ParamEditorEvent(ph_event.PEE_READ_PARAM))
        self.event_queue_lock.release()
        event.Skip()

    def write_param(self, event):  # wxGlade: ParamEditor.<event_handler>
        param = [param for param, value in self.modified_param.items()]
        self.event_queue_lock.acquire()
        self.event_queue.put(ParamEditorEvent(ph_event.PEE_WRITE_PARAM,
                                              modparam=self.modified_param))
        self.event_queue_lock.release()
        for row in range(self.display_list.GetNumberRows()):
            if self.display_list.GetCellValue(row, PE_PARAM) in param:
                self.display_list.SetCellBackgroundColour(row, PE_VALUE,
                                                          wx.Colour(255, 160, 90))
        event.Skip()

    def get_vehicle_type(self, name):
        self.vehicle_name = name
        self.param_help_tree()

    def key_change(self, event):  # wxGlade: ParamEditor.<event_handler>
        self.gui_event_queue_lock.acquire()
        key = self.search_key.GetValue()
        temp = {}
        for param, value in self.param_received.items():
            if key.lower() in param.lower():
                temp[param] = value
            else:
                try:
                    if key.lower() in (self.htree[param].get('documentation').lower() + self.htree[param].get('humanName').lower()):
                        temp[param] = value
                except Exception as e:
                    continue
        self.redraw_grid(temp)
        self.gui_event_queue_lock.release()
        event.Skip()

    def ParamChanged(self, event):  # wxGlade: ParamEditor.<event_handler>
        row_changed = event.GetRow()
        if event.Col == PE_OPTION:
            newval = float(self.display_list.GetCellValue(row_changed, PE_VALUE))
            self.display_list.SetCellValue(row_changed, PE_VALUE, str(round(newval, 4)))
        elif event.Col == PE_VALUE:
            newval = float(self.display_list.GetCellValue(row_changed, PE_VALUE))
            celleditor = self.display_list.GetCellEditor(row_changed, PE_OPTION)
            try:
                celleditor.set_checked(newval)
            except Exception as e:
                pass
        if float(self.oldval) != newval:
            self.display_list.SetCellBackgroundColour(row_changed, PE_VALUE,
                                                      wx.Colour(152, 251, 152))
            self.modified_param[self.display_list.GetCellValue(
                row_changed, PE_PARAM)] = newval
            self.param_received[self.display_list.GetCellValue(
                row_changed, PE_PARAM)] = newval
        event.Skip()

    def param_help_download(self):
        '''download XML files for parameters'''
        files = []
        for vehicle in ['APMrover2', 'ArduCopter', 'ArduPlane', 'ArduSub', 'AntennaTracker']:
            url = 'http://autotest.ardupilot.org/Parameters/%s/apm.pdef.xml' % vehicle
            path = mp_util.dot_mavproxy("%s.xml" % vehicle)
            files.append((url, path))
            url = 'http://autotest.ardupilot.org/%s-defaults.parm' % vehicle
            if vehicle != 'AntennaTracker':
                # defaults not generated for AntennaTracker ATM
                path = mp_util.dot_mavproxy("%s-defaults.parm" % vehicle)
                files.append((url, path))
        try:
            child = multiproc.Process(target=mp_util.download_files, args=(files,))
            child.start()
        except Exception as e:
            print(e)

    def param_help_tree(self):
        '''return a "help tree", a map between a parameter and its metadata.  May return None if help is not available'''
        if self.xml_filepath is not None:
            path = self.xml_filepath
        elif self.vehicle_name is not None:
            path = mp_util.dot_mavproxy("%s.xml" % self.vehicle_name)
            if not os.path.exists(path):
                self.param_help_download()
        else:
            return
        try:
            xml = open(path, 'rb').read()
            from lxml import objectify
            objectify.enable_recursive_str()
            tree = objectify.fromstring(xml)
            for p in tree.vehicles.parameters.param:
                n = p.get('name').split(':')[1]
                self.htree[n] = p
            for lib in tree.libraries.parameters:
                for p in lib.param:
                    n = p.get('name')
                    self.htree[n] = p
        except Exception as e:
            print (e)

# end of class ParamEditor


if __name__ == "__main__":
    app = wx.App(False)
    wx.InitAllImageHandlers()
    paramEditor = (None, wx.ID_ANY, "")
    app.SetTopWindow(paramEditor)
    paramEditor.Show()
    app.MainLoop()
