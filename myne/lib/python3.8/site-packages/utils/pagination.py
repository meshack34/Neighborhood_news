class Bullet(object):
    def __init__(self, number, link, active):
        self.number = number
        self.link = link
        self.active = active


class Paginator(object):
    def __init__(self, objects, page, get_link, per_page=20, bullets=5):
        page = int(page)
        self.page = page
        self.get_link = get_link
        self.all_objects = objects
        self.objects_count = objects.count()
        per_page = per_page() if callable(per_page) else per_page
        self.pages_count = int(float(self.objects_count) / float(per_page)) + 1
        self.bullets_count = 5
        self.per_page = per_page
        self.start = (page - 1) * per_page
        self.end = page * per_page
        self.is_first = page == 1
        self.first_bullet = Bullet(1, self.get_link(1), False)
        self.is_last = page == self.pages_count
        self.last_bullet = Bullet(self.pages_count, self.get_link(self.pages_count), False)
        self.has_pages = self.pages_count != 1
        self._objects = None
        self._bullets = None
        
    @property
    def bullets(self):
        if self._bullets is None:
            pre = int(float(self.bullets_count) / 2)
            bullets = [Bullet(self.page, self.get_link(self.page), True)]
            diff = 0
            for i in range(1, pre + 1):
                this = self.page - i
                if this:
                    bullets.insert(0, Bullet(this, self.get_link(this), False))
                else:
                    diff = pre - this
                    break
            for i in range(1, pre + 1 + diff):
                this = self.page +  i
                if this <= self.pages_count:
                    bullets.append(Bullet(this, self.get_link(this), False))
                else:
                    break
            self._bullets = bullets
        return self._bullets
        
    @property
    def objects(self):
        if self._objects is None:
            self._objects = self.all_objects[self.start:self.end]
        return self._objects