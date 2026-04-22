import random
import copy


class Resident:
    def __init__(self, name, room, student_id, photo_id=None):
        self.name = name
        self.room = room
        self.student_id = student_id
        self.photo_id = photo_id
        self.display_photo = photo_id
        self.id_card = self._generate_card()

    def _generate_card(self):
        return {
            "name":       self.name,
            "room":       self.room,
            "student_id": self.student_id,
            "photo_id":   self.photo_id,
        }

    def validate(self):
        errors = []

        if not self.name or not isinstance(self.name, str):
            errors.append("Invalid name")
        if not self.room or not str(self.room).isdigit():
            errors.append("Invalid room number")
        if not self.student_id or not self.student_id.startswith("STU"):
            errors.append("Invalid student ID format (must start with STU)")
        if self.photo_id and not self.photo_id.endswith(".png"):
            errors.append("Invalid photo format (must be .png)")

        return len(errors) == 0, errors

    def display_card(self, screen, fonts, x, y):
        import pygame
        pygame.draw.rect(screen, (240, 240, 240),
                         (x, y, 300, 200), border_radius=8)
        pygame.draw.rect(screen, (70, 114, 196),
                         (x, y, 300, 200), width=2, border_radius=8)

        if self.photo_id:
            img = pygame.image.load(f"assets/faces/{self.photo_id}")
            img = pygame.transform.scale(img, (80, 80))
            screen.blit(img, (x + 10, y + 10))
        else:
            pygame.draw.rect(screen, (180, 180, 180), (x + 10, y + 10, 80, 80))

        screen.blit(fonts["normal"].render(
            f"Name: {self.id_card['name']}",       True, (0, 0, 0)), (x + 100, y + 20))
        screen.blit(fonts["normal"].render(
            f"Room: {self.id_card['room']}",       True, (0, 0, 0)), (x + 100, y + 50))
        screen.blit(fonts["normal"].render(
            f"ID:   {self.id_card['student_id']}", True, (0, 0, 0)), (x + 100, y + 80))

    def to_dict(self):
        return {
            "name":       self.name,
            "room":       self.room,
            "student_id": self.student_id,
            "photo_id":   self.photo_id,
        }

    def get_result(self):
        return True

    def __repr__(self):
        return f"Resident({self.name}, Room {self.room})"


class Doppelganger(Resident):

    ERROR_TYPES = ["room_mismatch", "name_error",
                   "name_typo", "wrong_id", "photo_swap"]

    def __init__(self, resident, error_type=None):
        super().__init__(
            name=resident.name,
            room=resident.room,
            student_id=resident.student_id,
            photo_id=resident.photo_id,
        )
        if self.photo_id:
            base = self.photo_id.replace(".png", "")
            self.display_photo = f"{base}_dop.png"
        self.original_data = resident.to_dict()
        self.error_type = error_type or random.choice(self.ERROR_TYPES)
        self.disguise_level = 1

        self.generate_error()

    def generate_error(self):
        if self.error_type == "room_mismatch":
            self.room = str(int(self.room) + random.choice([-1, 1]))

        elif self.error_type == "name_error":
            fake_names = ["John Smyth", "Maria Garsia",
                          "James Li", "Sara Jonson", "David Kin"]
            self.name = random.choice(
                [n for n in fake_names if n != self.name])

        elif self.error_type == "name_typo":
            name = list(self.name)
            idx = random.randint(0, len(name) - 1)
            name[idx] = random.choice("abcdefghijklmnopqrstuvwxyz")
            self.name = "".join(name)

        elif self.error_type == "wrong_id":
            last_digit = int(self.student_id[-1])
            new_digit = random.choice([d for d in range(10) if d != last_digit])
            self.student_id = self.student_id[:-1] + str(new_digit)

        elif self.error_type == "photo_swap":
            all_photos = ["stu001.png", "stu002.png",
                          "stu003.png", "stu004.png", "stu005.png"]
            self.photo_id = random.choice(
                [p for p in all_photos if p != self.photo_id])
            base = self.photo_id.replace(".png", "")
            self.display_photo = f"{base}_dop.png"

        self.id_card = self._generate_card()

    def get_mismatch(self):
        mismatches = []
        if self.name != self.original_data["name"]:
            mismatches.append(
                f"name: '{self.original_data['name']}' → '{self.name}'")
        if self.room != self.original_data["room"]:
            mismatches.append(
                f"room: '{self.original_data['room']}' → '{self.room}'")
        if self.student_id != self.original_data["student_id"]:
            mismatches.append(
                f"student_id: '{self.original_data['student_id']}' → '{self.student_id}'")
        if self.photo_id != self.original_data["photo_id"]:
            mismatches.append(
                f"photo: '{self.original_data['photo_id']}' → '{self.photo_id}'")
        return mismatches

    def get_result(self):
        return False

    def __repr__(self):
        return f"Doppelganger({self.name}, Room {self.room}, error={self.error_type})"
