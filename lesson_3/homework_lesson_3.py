import pygame

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dodger_blue = (30, 144, 255)

dark_red = (200, 0, 0)
dark_green = (0, 200, 0)
orange = (255, 165, 0 )

screen_size = (display_width, display_height)
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

free_sans_normal = pygame.font.Font("FreeSans.ttf", 14)
free_sans_medium = pygame.font.Font("FreeSans.ttf", 24)
free_sans_large = pygame.font.Font("FreeSans.ttf", 32)

def draw_text_button(x, y, w, h, text, clickable = True):
  m_point = pygame.mouse.get_pos()
  m_click = pygame.mouse.get_pressed()
  action_intent = False

  if clickable and pygame.Rect((x, y), (w, h)).collidepoint(m_point):
    pygame.draw.rect(screen, orange, (x, y, w, h))
    if m_click[0] == 1:
      action_intent = True
  else:
    pygame.draw.rect(screen, dodger_blue, (x, y, w, h))

  text_surface = free_sans_normal.render(text, True, white)
  text_rect = text_surface.get_rect()
  text_rect.center = ( (x + w / 2), (y + h / 2) )

  screen.blit(text_surface, text_rect)

  return action_intent


def draw_text(x, y, font, text):
  text_surface = font.render(text, True, black)
  text_rect = text_surface.get_rect()
  text_rect.center = ( x, y )
  screen.blit(text_surface, text_rect)


def show_question(index):
  text = questions[index]
  draw_text(display_width / 2, 50, free_sans_medium, text)


def show_answers(index, guessed = False):
  correct = corrects[index]
  options = answers[index]
  option_a = options[0]
  option_b = options[1]
  option_c = options[2]
  option_d = options[3]

  if guessed:
    if correct == 'a':
      draw_text_button(60, 400, 340, 40, option_a, False)
    elif correct == 'b':
      draw_text_button(420, 400, 340, 40, option_b, False)
    elif correct =='c':
      draw_text_button(60, 500, 340, 40, option_c, False)
    else:
      draw_text_button(420, 500, 340, 40, option_d, False)
  else:
    click_on_a = draw_text_button(60, 400, 340, 40, option_a)
    click_on_b = draw_text_button(420, 400, 340, 40, option_b)
    click_on_c = draw_text_button(60, 500, 340, 40, option_c)
    click_on_d = draw_text_button(420, 500, 340, 40, option_d)
    
    if click_on_a:
      pygame.event.post(pygame.event.Event(GUESS_A))
    elif click_on_b:
      pygame.event.post(pygame.event.Event(GUESS_B))
    elif click_on_c:
      pygame.event.post(pygame.event.Event(GUESS_C))
    elif click_on_d:
      pygame.event.post(pygame.event.Event(GUESS_D))

def show_winner():
  draw_text(display_width / 2, 100, free_sans_large, 'Correct!')


def show_looser():
  draw_text(display_width / 2, 100, free_sans_large, '#Noob')


def show_scores(scores):
  text = '{} Pont a griffendélnek'.format(scores)
  draw_text(display_width / 2, 100, free_sans_large, text)


def show_next_question_button():
  click_on = draw_text_button(20, 300, 760, 60, 'Következő kérdés')
  if click_on:
    pygame.event.post(pygame.event.Event(NEXT_Q_EVENT))


questions = [
    'Vajon hány kérdésre tudod majd a választ?',
    'Milyen színű volt Radagast, a mágus?',
    'Hogy kell helyesen írni Ausztrália fővárosát?',
    'Hányadik Season-nál tart a Diablo 3?',
    'Melyik játék főhősei olasz vízszerelők?',
    'Melyik animeben hangzott el: ,,Készülj a harcra és vele a kudarcra...'' ',
    'Melyik nem DC-s karakter?'
]

answers = [
    ['Az összesre', 'Legalább a felére', 'Örülök, ha csak egyre', 'Ez kérdés?!'],
    ['Szürke', 'Fehér', 'Barna', 'Fekete'],
    ['Sidnei', 'Sydney', 'Sidney', 'Egyik sem helyes'],
    ['16', '13', '2', '19'],
    ['Donkey Kong', 'Super Mario', 'Zelda', 'Call of Duty'],
    ['Sailor Moon', 'Dragon Ball', 'Pokemon', 'Castlevania'],
    ['Superman', 'Black Canary', 'Ant', 'Raven']
]

corrects = [
    'd',
    'c',
    'd',
    'a',
    'b',
    'c',
    'c'
]

NEXT_Q_EVENT = pygame.USEREVENT + 1
GUESS_A = pygame.USEREVENT + 2
GUESS_B = pygame.USEREVENT + 3
GUESS_C = pygame.USEREVENT + 4
GUESS_D = pygame.USEREVENT + 5

def game_loop():
  game = {
    'paused': False,
    'winner': False,
    'looser': False,
    'game_over': False,
    'current_question': 0,
    'current_points': 0
  }

  def user_guessed(guess):
    game['paused'] = True
    pygame.time.set_timer(NEXT_Q_EVENT, 10000)
    
    if guess == corrects[game['current_question']]:
      game['current_points'] = game['current_points'] + 1
      game['winner'] = True
    else:
      game['looser'] = True

  def next_question():
    game['paused'] = False
    game['winner'] = False
    game['looser'] = False

    game['current_question'] += 1
    if game['current_question'] >= len(questions):
      game['game_over'] = True
      
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == GUESS_A:
        user_guessed ('a')
        
      if event.type == GUESS_B:
        user_guessed ('b')
        
      if event.type == GUESS_C:
        user_guessed ('c')
        
      if event.type == GUESS_D:
        user_guessed ('d')

      if game ['paused'] and event.type == NEXT_Q_EVENT:
        next_question ()
      
    screen.fill(white)

    if game ['game_over']:
      show_scores (game ['current_points'])
    else:
      show_question(game['current_question'])
      show_answers(game['current_question'], game ['paused'])

      if game ['winner']:
        show_winner ()

      if game ['looser']:
        show_looser ()

      if game ['paused']:
        show_next_question_button ()
      
     
    pygame.display.update()
    clock.tick(15)
    

game_loop()
