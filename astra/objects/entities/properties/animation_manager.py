class AnimationManager:
    def __init__(self, entity, delta):
        self.delta = delta
        self.entity = entity
        self.current_frame = 0
        self.animation_time = 0
        self.frame_duration = .5

    def get_sprite_list(self, state, orientation):
        sprite_manager = self.entity.sprite_manager
        return getattr(sprite_manager, f"{state}_{orientation}")

    def update_frame(self, sprite_list):
        self.current_frame = (self.current_frame + 1) % len(sprite_list)

    def update(self):
        self.update_animation_time()
        if self.animation_time >= self.frame_duration:
            self.adjust_animation_time()
            state = self.determine_state()
            sprite_list = self.get_sprite_list(state, self.entity.orientation)
            self.update_frame(sprite_list)
            self.reset_state_if_attacking()

    def update_animation_time(self):
        self.animation_time += self.delta / 1000

    def adjust_animation_time(self):
        self.animation_time -= self.frame_duration

    def determine_state(self):
        return "attack" if self.entity.state == "attacking" else "idle"

    def reset_state_if_attacking(self):
        if self.entity.state == "attacking" and self.current_frame == 0:
            self.entity.state = "idle"
