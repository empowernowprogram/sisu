from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):

    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return [
            'index',
            'about-us',
            'contact',
            'faq',
        ]

    def priority(self, item):
        return {
            'index': 1.0, 
            'about-us': 0.8, 
            'contact': 0.5, 
            'faq': 0.5}[item]

    def location(self, item):
        return reverse(item)