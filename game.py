import pygame
import random
import sys

class DoorQuizGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Screen dimensions
        self.screen_width = 800
        self.screen_height = 600

        # Set up the display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Edward's Discord Learning")

        # Load character image
        try:
            self.character_img = pygame.image.load('character.png')
        except pygame.error:
            self.character_img = pygame.Surface((30, 50))
            self.character_img.fill((255, 165, 0))

        # Load sounds
        try:
            self.walking_sound = pygame.mixer.Sound('walking.wav')
            self.door_sound = pygame.mixer.Sound('door.wav')
            self.wrong_answer_sound = pygame.mixer.Sound('wrong.wav')
            self.game_over_sound = pygame.mixer.Sound('gameover.wav')
            pygame.mixer.music.load('background.mp3')  # Load the background music file
            pygame.mixer.music.play(-1)  # Play the music in a loop
            pygame.mixer.music.set_volume(0.3)  # Set background music volume (30%)
        except pygame.error:
            self.walking_sound = None
            self.door_sound = None
            self.wrong_answer_sound = None
            self.game_over_sound = None

        self.character_rect = self.character_img.get_rect()
        self.character_rect.center = (100, self.screen_height - 150)

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BROWN = (139, 69, 19)

        # Font
        self.font = pygame.font.SysFont(None, 36)

        # Game variables
        self.lives = 5
        self.score = 0
        self.current_question = 0
        self.current_door_open = False
        self.door_animation_progress = 0

        # Door variables
        self.door_width = 100
        self.door_height = 200
        self.door_start_x = 300
        self.character_start_x = 100

        # Questions
        self.questions = [
            {"question": "What is a Discord server?", "answers": ["A place to chat", "A type of food", "A video game"], "correct": 0},
            {"question": "How do you create a channel?", "answers": ["Use the + icon", "Use the - icon", "Use the * icon"], "correct": 0},
            {"question": "What is a Discord bot?", "answers": ["Automated assistant", "Voice filter", "Video player"], "correct": 0},
            {"question": "What is the maximum file upload size for free users?", "answers": ["8MB", "50MB", "100MB"], "correct": 0},
            {"question": "What is a server template?", "answers": ["Pre-made setup", "Bot config", "Role list"], "correct": 0},
            {"question": "What is slowmode?", "answers": ["Message delay", "Voice limit", "Upload restriction"], "correct": 0},
            {"question": "What is a server banner?", "answers": ["Header image", "Role icon", "Emoji pack"], "correct": 0},
            {"question": "What are server emojis?", "answers": ["Custom emoticons", "Role icons", "Bot commands"], "correct": 0},
            {"question": "What is a category?", "answers": ["Channel group", "Role type", "Server region"], "correct": 0},
            {"question": "What is an announcement channel?", "answers": ["News broadcast", "Voice chat", "DM group"], "correct": 0},
            {"question": "What is a server nickname?", "answers": ["Custom username", "Bot name", "Channel name"], "correct": 0},
            {"question": "What is a Discord partner?", "answers": ["Official partner", "Premium user", "Server owner"], "correct": 0},
            {"question": "What is a stage channel?", "answers": ["Presentation room", "Gaming chat", "Music bot"], "correct": 0},
            {"question": "What is a server boost level?", "answers": ["Perks tier", "User rank", "Bot status"], "correct": 0},
            {"question": "What is a server region?", "answers": ["Server location", "Time zone", "Language setting"], "correct": 0},
            {"question": "What is a Discord badge?", "answers": ["Profile icon", "Server rank", "Message type"], "correct": 0},
            {"question": "What is a Discord overlay?", "answers": ["Game HUD", "Voice display", "Server list"], "correct": 0},
            {"question": "What is Rich Presence?", "answers": ["Game status", "Server status", "User status"], "correct": 0},
            {"question": "What is a server widget?", "answers": ["Embed display", "Bot command", "Role menu"], "correct": 0},
            {"question": "What is server boosting?", "answers": ["Adding perks", "Deleting a server", "Creating new roles"], "correct": 0},
            {"question": "What is Discord's mascot called?", "answers": ["Wumpus", "Blorg", "Nitro"], "correct": 0},
            {"question": "What is the purpose of a webhook in Discord?", "answers": ["Send automated messages", "Change server region", "Play music"], "correct": 0},
            {"question": "What is the maximum character limit for a Discord message?", "answers": ["2000", "5000", "1000"], "correct": 0},
            {"question": "What is a role hierarchy used for in Discord?", "answers": ["Determining permissions", "Changing channel themes", "Setting member limits"], "correct": 0},
            {"question": "What is the primary function of Discord Nitro?", "answers": ["Enhance user experience", "Ban unwanted members", "Host servers"], "correct": 0},
            {"question": "What is a Discord audit log?", "answers": ["Activity history", "Role editor", "Emote list"], "correct": 0},
            {"question": "What is the color of the online status icon in Discord?", "answers": ["Green", "Blue", "Red"], "correct": 0},
            {"question": "What is the maximum number of people in a video call on Discord?", "answers": ["25", "50", "10"], "correct": 0},
            {"question": "What is the function of a category in Discord?", "answers": ["Organize channels", "Boost server speed", "Send mass messages"], "correct": 0},
            {"question": "What feature is used to create a sub-discussion in Discord?", "answers": ["Thread", "Poll", "Boost"], "correct": 0},
        ]
        self.shuffle_questions()

    def shuffle_questions(self):
        for question in self.questions:
            answers = question["answers"]
            correct_index = question["correct"]
            # Pair answers with their indices, shuffle them, and update the question
            paired_answers = list(enumerate(answers))
            random.shuffle(paired_answers)
            question["answers"] = [ans for _, ans in paired_answers]
            question["correct"] = [i for i, (idx, _) in enumerate(paired_answers) if idx == correct_index][0]

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_door(self, x, y, width, height, is_open):
        if is_open:
            pygame.draw.rect(self.screen, self.GREEN, (x, y, width, height))
        else:
            pygame.draw.rect(self.screen, self.BROWN, (x, y, width, height))

    def move_character_towards(self, target_x, speed):
        if self.character_rect.centerx < target_x:
            self.character_rect.x += min(speed, target_x - self.character_rect.centerx)
            if self.walking_sound and not pygame.mixer.get_busy():
                self.walking_sound.play()
        return self.character_rect.centerx >= target_x

    def reset_positions(self):
        self.character_rect.center = (self.character_start_x, self.screen_height - 150)

    def game_over_animation(self):
        """Play game over animation."""
        if self.game_over_sound:
            self.game_over_sound.play()
        for i in range(100):
            self.screen.fill(self.BLACK)
            scale = max(5, 100 - i)
            rotated_image = pygame.transform.rotate(self.character_img, i * 10)
            scaled_image = pygame.transform.scale(rotated_image, (scale, scale))
            rect = scaled_image.get_rect(center=(random.randint(0, self.screen_width), random.randint(0, self.screen_height)))
            self.screen.blit(scaled_image, rect.topleft)
            pygame.display.flip()
            pygame.time.delay(50)
        self.display_game_over_text()

    def display_game_over_text(self):
        """Display 'Game Over' text."""
        self.screen.fill(self.BLACK)
        game_over_text = self.font.render("Game Over!", True, self.RED)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, self.WHITE)
        self.screen.blit(game_over_text, (self.screen_width // 2 - 100, self.screen_height // 3))
        self.screen.blit(final_score_text, (self.screen_width // 2 - 120, self.screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

    def run(self):
        running = True
        question_active = True
        answer_rects = []
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(self.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and question_active:
                    mouse_pos = event.pos
                    for i, answer_rect in enumerate(answer_rects):
                        if answer_rect.collidepoint(mouse_pos):
                            if i == self.questions[self.current_question]["correct"]:
                                self.current_door_open = True
                                question_active = False
                                self.score += 1
                                if self.door_sound:
                                    self.door_sound.play()
                                self.door_animation_progress = 0
                            else:
                                if self.wrong_answer_sound:
                                    self.wrong_answer_sound.play()
                                self.lives -= 1
                                if self.lives <= 0:
                                    self.game_over_animation()
                                    running = False

            # Calculate door position
            door_x = self.door_start_x
            door_y = self.screen_height - 250

            if not question_active:
                if self.current_door_open:
                    door_reached = self.move_character_towards(door_x + self.door_width + 20, 5)
                    if door_reached:
                        self.reset_positions()
                        self.current_door_open = False
                        question_active = True
                        self.current_question += 1
                        if self.current_question >= len(self.questions):
                            running = False

            # Draw door
            self.draw_door(door_x, door_y, self.door_width, self.door_height, self.current_door_open)

            # Draw character
            self.screen.blit(self.character_img, self.character_rect)

            # Draw UI
            self.draw_text(f"Lives: {self.lives}", self.RED, 10, 10)
            self.draw_text(f"Score: {self.score}", self.GREEN, self.screen_width - 120, 10)
            self.draw_text(f"Question: {self.current_question + 1}/{len(self.questions)}", self.WHITE, self.screen_width // 2 - 100, 10)

            # Display question
            if question_active and self.current_question < len(self.questions):
                question = self.questions[self.current_question]
                self.draw_text(question["question"], self.WHITE, 50, 50)
                answer_rects = []
                for i, answer in enumerate(question["answers"]):
                    answer_text = self.font.render(answer, True, self.WHITE)
                    answer_rect = answer_text.get_rect()
                    answer_rect.topleft = (50, 150 + i * 40)
                    self.screen.blit(answer_text, answer_rect.topleft)
                    answer_rects.append(answer_rect)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()

# Main execution
if __name__ == "__main__":
    game = DoorQuizGame()
    game.run()
