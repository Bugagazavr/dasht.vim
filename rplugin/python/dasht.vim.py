import neovim

@neovim.plugin
class Dasht(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.default_window = None
        self.dasht_window = None

    @neovim.command("Dasht", nargs='*', sync=True)
    def dashtcommand(self, args):
        if self.dasht_window == None:
            self.create_new_dasht_window(args)
        else:
            try:
                self.nvim.current.window = self.dasht_window
                self.nvim.command('close')
                self.create_new_dasht_window(args)
            except neovim.api.nvim.NvimError:
                self.dasht_window = None
                self.create_new_dasht_window(args)

    def create_new_dasht_window(self, args):
        self.nvim.command('belowright split')

        try:
            last_window = self.nvim.windows.__len__() - 1

            self.dasht_window = self.nvim.windows.__getitem__(last_window)
        except IndexError:
            self.dasht_window = None

        if self.dasht_window != None:
            self.set_window(args)

    def set_window(self, args):
        try:
            self.nvim.current.window = self.dasht_window
            self.nvim.command('enew')
            self.nvim.funcs.termopen('dasht %s' % ' '.join(args))
            self.nvim.command('startinsert')
        except neovim.api.nvim.NvimError:
            self.dasht_window = None
            self.create_new_dasht_window(args)
