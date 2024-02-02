class AnimationManager:
    def __init__(self, entity):
        self.entity = entity
        self.current_frame = 0
        self.animation_time = 0
        self.frame_duration = .5

    def update(self):
        self.animation_time += self.entity.game.delta / 1000
        if self.animation_time >= self.frame_duration:
            self.animation_time -= self.frame_duration
            if self.entity.state == "attacking":
                self.current_frame = (
                    (self.current_frame + 1) % len(self.entity.attack_d)
                    if self.entity.orientation == "down"
                    else (self.current_frame + 1) % len(self.entity.attack_u)
                )
                if self.current_frame == 0:
                    self.entity.state = "idle"
            elif self.entity.orientation == "down":
                self.current_frame = (self.current_frame + 1) % len(self.entity.idle_d)
            else:
                self.current_frame = (self.current_frame + 1) % len(self.entity.idle_u)