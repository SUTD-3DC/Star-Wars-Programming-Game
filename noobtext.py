from pygame.locals import *
import pygame, string

class Textbox:

    def __init__(self, lines=1, **options):
        
        self.txtbx = []
        self.foci = 0
        self.cursor_pos = []

        y_pos = 0
        if 'y' in options.keys():
            y_pos = options['y']

        for line in range(lines):
            self.txtbx.append(Input(**options))
            y_pos += 20
            options['y'] = y_pos

            self.cursor_pos.append(0)

        self.txtbx[self.foci].focus = True

    def update(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.txtbx[self.foci].focus = False
                    old_cursor = self.txtbx[self.foci].get_cursor()
                    self.cursor_pos[self.foci] = old_cursor
                    self.foci += 1
                    self.foci %= len(self.txtbx)
                    self.txtbx[self.foci].set_cursor(old_cursor)
                    self.cursor_pos[self.foci] = self.txtbx[self.foci].get_cursor()
                    self.txtbx[self.foci].focus = True
                elif event.key == K_UP:
                    self.txtbx[self.foci].focus = False
                    old_cursor = self.txtbx[self.foci].get_cursor()
                    self.cursor_pos[self.foci] = old_cursor
                    self.foci -= 1
                    self.foci %= len(self.txtbx)
                    self.txtbx[self.foci].set_cursor(old_cursor)
                    self.cursor_pos[self.foci] = self.txtbx[self.foci].get_cursor()
                    self.txtbx[self.foci].focus = True
                elif event.key == K_DOWN:
                    self.txtbx[self.foci].focus = False
                    old_cursor = self.txtbx[self.foci].get_cursor()
                    self.cursor_pos[self.foci] = old_cursor
                    self.foci += 1
                    self.foci %= len(self.txtbx)
                    self.txtbx[self.foci].set_cursor(old_cursor)
                    self.cursor_pos[self.foci] = self.txtbx[self.foci].get_cursor()
                    self.txtbx[self.foci].focus = True
                elif event.key == K_LEFT:
                    self.txtbx[self.foci].move_cursor_relative(-1)
                elif event.key == K_RIGHT:
                    self.txtbx[self.foci].move_cursor_relative(1)
        self.txtbx[self.foci].update(events)

    def draw(self, screen):
        for txt in self.txtbx:
            txt.draw(screen)

    def get(self):
        return self.txtbx


class ConfigError(KeyError): pass

class Config:
    """ A utility for configuration """
    def __init__(self, options, *look_for):
        assertions = []
        for key in look_for:
            if key[0] in options.keys(): exec('self.'+key[0]+' = options[\''+key[0]+'\']')
            else: exec('self.'+key[0]+' = '+key[1])
            assertions.append(key[0])
        for key in options.keys():
            if key not in assertions: raise ConfigError(key+' not expected as option')

class Input:
    """ A text input for pygame apps """
    def __init__(self, **options):
        """ Options: x, y, font, color, restricted, maxlength, prompt """
        self.options = Config(options, ['x', '0'], ['y', '0'], ['font','pygame.font.Font("cour.ttf", 16)'],
                              ['color', '(0,0,0)'], ['restricted',
 '\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~\''],
                              ['maxlength', '-1'], ['prompt', '\'\''],['focus','False'])
        self.x = self.options.x; self.y = self.options.y
        self.font = self.options.font
        self.color = self.options.color
        self.restricted = self.options.restricted
        self.maxlength = self.options.maxlength
        self.prompt = self.options.prompt; self.value = ''
        self.shifted = False
        self.pause = 0
        self.focus = self.options.focus
        self.bar = False
        self.cursor_pos = 0

    def set_pos(self, x, y):
        """ Set the position to x, y """
        self.x = x
        self.y = y

    def set_font(self, font):
        """ Set the font for the input """
        self.font = font

    def get_cursor(self):
        return self.cursor_pos

    def set_cursor(self, cursor_pos):
        self.cursor_pos = cursor_pos
        if self.cursor_pos < 0:
            self.cursor_pos = 0
        if self.cursor_pos > len(self.value):
            self.cursor_pos = len(self.value)

    def _move_cursor_relative(self, dx, end):
        self.cursor_pos += dx
        if self.cursor_pos < 0:
            self.cursor_pos = 0
        if self.cursor_pos > end:
            self.cursor_pos = end

    def move_cursor_relative(self, dx):
        self._move_cursor_relative(dx, self.maxlength)

    def delete_char(self):
        if self.cursor_pos > 0:
            self.value = self.value[:self.cursor_pos-1] + self.value[self.cursor_pos:]

    def insert_char(self, c):
        self.value = self.value[:self.cursor_pos] + c + self.value[self.cursor_pos:]

    def draw(self, surface):
        """ Draw the text input to a surface """
        text = self.font.render(self.prompt+self.value, 1, self.color)
        surface.blit(text, (self.x, self.y))

    def update(self, events):
        """ Update the input based on passed events """
        if self.focus != True:
            return

        for event in events:
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
            if event.type == KEYDOWN: #S: Removes cursor when new letter is typed
                cursor_dx = 1
                if event.key == K_BACKSPACE:
                    self.delete_char()
                    cursor_dx = -1
                elif event.key == K_TAB:
                    self.insert_char('    ')
                    cursor_dx = 4
                elif event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = True
                elif event.key == K_SPACE:
                    self.insert_char(' ')
                    cursor_dx = 1
                elif event.key == K_RETURN: return self.value#return value
                if not self.shifted:
                    # if event.key == K_a and 'a' in self.restricted: self.value += 'a'
                    if event.key == K_a and 'a' in self.restricted: self.insert_char('a')
                    elif event.key == K_b and 'b' in self.restricted: self.insert_char('b')
                    elif event.key == K_c and 'c' in self.restricted: self.insert_char('c')
                    elif event.key == K_d and 'd' in self.restricted: self.insert_char('d')
                    elif event.key == K_e and 'e' in self.restricted: self.insert_char('e')
                    elif event.key == K_f and 'f' in self.restricted: self.insert_char('f')
                    elif event.key == K_g and 'g' in self.restricted: self.insert_char('g')
                    elif event.key == K_h and 'h' in self.restricted: self.insert_char('h')
                    elif event.key == K_i and 'i' in self.restricted: self.insert_char('i')
                    elif event.key == K_j and 'j' in self.restricted: self.insert_char('j')
                    elif event.key == K_k and 'k' in self.restricted: self.insert_char('k')
                    elif event.key == K_l and 'l' in self.restricted: self.insert_char('l')
                    elif event.key == K_m and 'm' in self.restricted: self.insert_char('m')
                    elif event.key == K_n and 'n' in self.restricted: self.insert_char('n')
                    elif event.key == K_o and 'o' in self.restricted: self.insert_char('o')
                    elif event.key == K_p and 'p' in self.restricted: self.insert_char('p')
                    elif event.key == K_q and 'q' in self.restricted: self.insert_char('q')
                    elif event.key == K_r and 'r' in self.restricted: self.insert_char('r')
                    elif event.key == K_s and 's' in self.restricted: self.insert_char('s')
                    elif event.key == K_t and 't' in self.restricted: self.insert_char('t')
                    elif event.key == K_u and 'u' in self.restricted: self.insert_char('u')
                    elif event.key == K_v and 'v' in self.restricted: self.insert_char('v')
                    elif event.key == K_w and 'w' in self.restricted: self.insert_char('w')
                    elif event.key == K_x and 'x' in self.restricted: self.insert_char('x')
                    elif event.key == K_y and 'y' in self.restricted: self.insert_char('y')
                    elif event.key == K_z and 'z' in self.restricted: self.insert_char('z')
                    elif event.key == K_0 and '0' in self.restricted: self.insert_char('0')
                    elif event.key == K_1 and '1' in self.restricted: self.insert_char('1')
                    elif event.key == K_2 and '2' in self.restricted: self.insert_char('2')
                    elif event.key == K_3 and '3' in self.restricted: self.insert_char('3')
                    elif event.key == K_4 and '4' in self.restricted: self.insert_char('4')
                    elif event.key == K_5 and '5' in self.restricted: self.insert_char('5')
                    elif event.key == K_6 and '6' in self.restricted: self.insert_char('6')
                    elif event.key == K_7 and '7' in self.restricted: self.insert_char('7')
                    elif event.key == K_8 and '8' in self.restricted: self.insert_char('8')
                    elif event.key == K_9 and '9' in self.restricted: self.insert_char('9')
                    elif event.key == K_BACKQUOTE and '`' in self.restricted: self.insert_char('`')
                    elif event.key == K_MINUS and '-' in self.restricted: self.insert_char('-')
                    elif event.key == K_EQUALS and '=' in self.restricted: self.insert_char('=')
                    elif event.key == K_LEFTBRACKET and '[' in self.restricted: self.insert_char('[')
                    elif event.key == K_RIGHTBRACKET and ']' in self.restricted: self.insert_char(']')
                    elif event.key == K_BACKSLASH and '\\' in self.restricted: self.insert_char('\\')
                    elif event.key == K_SEMICOLON and ';' in self.restricted: self.insert_char(';')
                    elif event.key == K_QUOTE and '\'' in self.restricted: self.insert_char('\'')
                    elif event.key == K_COMMA and ',' in self.restricted: self.insert_char(',')
                    elif event.key == K_PERIOD and '.' in self.restricted: self.insert_char('.')
                    elif event.key == K_SLASH and '/' in self.restricted: self.insert_char('/')
                    else:
                        if event.key != K_BACKSPACE and \
                           event.key != K_TAB and \
                           event.key != K_SPACE:
                               cursor_dx = 0
                elif self.shifted:
                    if event.key == K_a and 'A' in self.restricted: self.insert_char('A')
                    elif event.key == K_b and 'B' in self.restricted: self.insert_char('B')
                    elif event.key == K_c and 'C' in self.restricted: self.insert_char('C')
                    elif event.key == K_d and 'D' in self.restricted: self.insert_char('D')
                    elif event.key == K_e and 'E' in self.restricted: self.insert_char('E')
                    elif event.key == K_f and 'F' in self.restricted: self.insert_char('F')
                    elif event.key == K_g and 'G' in self.restricted: self.insert_char('G')
                    elif event.key == K_h and 'H' in self.restricted: self.insert_char('H')
                    elif event.key == K_i and 'I' in self.restricted: self.insert_char('I')
                    elif event.key == K_j and 'J' in self.restricted: self.insert_char('J')
                    elif event.key == K_k and 'K' in self.restricted: self.insert_char('K')
                    elif event.key == K_l and 'L' in self.restricted: self.insert_char('L')
                    elif event.key == K_m and 'M' in self.restricted: self.insert_char('M')
                    elif event.key == K_n and 'N' in self.restricted: self.insert_char('N')
                    elif event.key == K_o and 'O' in self.restricted: self.insert_char('O')
                    elif event.key == K_p and 'P' in self.restricted: self.insert_char('P')
                    elif event.key == K_q and 'Q' in self.restricted: self.insert_char('Q')
                    elif event.key == K_r and 'R' in self.restricted: self.insert_char('R')
                    elif event.key == K_s and 'S' in self.restricted: self.insert_char('S')
                    elif event.key == K_t and 'T' in self.restricted: self.insert_char('T')
                    elif event.key == K_u and 'U' in self.restricted: self.insert_char('U')
                    elif event.key == K_v and 'V' in self.restricted: self.insert_char('V')
                    elif event.key == K_w and 'W' in self.restricted: self.insert_char('W')
                    elif event.key == K_x and 'X' in self.restricted: self.insert_char('X')
                    elif event.key == K_y and 'Y' in self.restricted: self.insert_char('Y')
                    elif event.key == K_z and 'Z' in self.restricted: self.insert_char('Z')
                    elif event.key == K_0 and ')' in self.restricted: self.insert_char(')')
                    elif event.key == K_1 and '!' in self.restricted: self.insert_char('!')
                    elif event.key == K_2 and '@' in self.restricted: self.insert_char('@')
                    elif event.key == K_3 and '#' in self.restricted: self.insert_char('#')
                    elif event.key == K_4 and '$' in self.restricted: self.insert_char('$')
                    elif event.key == K_5 and '%' in self.restricted: self.insert_char('%')
                    elif event.key == K_6 and '^' in self.restricted: self.insert_char('^')
                    elif event.key == K_7 and '&' in self.restricted: self.insert_char('&')
                    elif event.key == K_8 and '*' in self.restricted: self.insert_char('*')
                    elif event.key == K_9 and '(' in self.restricted: self.insert_char('(')
                    elif event.key == K_BACKQUOTE and '~' in self.restricted: self.insert_char('~')
                    elif event.key == K_MINUS and '_' in self.restricted: self.insert_char('_')
                    elif event.key == K_EQUALS and '+' in self.restricted: self.insert_char('+')
                    elif event.key == K_LEFTBRACKET and '{' in self.restricted: self.insert_char('{')
                    elif event.key == K_RIGHTBRACKET and '}' in self.restricted: self.insert_char('}')
                    elif event.key == K_BACKSLASH and '|' in self.restricted: self.insert_char('|')
                    elif event.key == K_SEMICOLON and ':' in self.restricted: self.insert_char(':')
                    elif event.key == K_QUOTE and '"' in self.restricted: self.insert_char('"')
                    elif event.key == K_COMMA and '<' in self.restricted: self.insert_char('<')
                    elif event.key == K_PERIOD and '>' in self.restricted: self.insert_char('>')
                    elif event.key == K_SLASH and '?' in self.restricted: self.insert_char('?')
                    else:
                        if event.key != K_BACKSPACE and \
                           event.key != K_TAB and \
                           event.key != K_SPACE:
                               cursor_dx = 0
                self._move_cursor_relative(cursor_dx, len(self.value))
                print self.cursor_pos

        if len(self.value) > self.maxlength and self.maxlength >= 0: self.value = self.value[:-1]
