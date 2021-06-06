import pygal

from .models import Category, Post
from pygal.style import DefaultStyle

class CatPieChart():
  def __init__(self, **kwargs):
      self.chart = pygal.Pie(**kwargs)
      self.chart.print_values = True
      #self.chart.title = 'You Activity'
        
  def get_data(self, user_data):
      data = {}
      categories = Category.__members__.items()
           
      for name, member in categories:
        data[member.value] = 0
        #print("in chart.py: " + member.label + " " + name)
           
      for post in user_data:
        print(post.category_name)
        if(post.category_name.name in data):
          data[post.category_name.name] += 1
        else:
          data[post.category_name.name] = 1
      
      return data
  
  def generate(self, user_data):
      chart_data = self.get_data(user_data)
      self.chart = pygal.Pie(print_values=True, style=DefaultStyle(
                    legend_font_family = 'googlefont:Raleway',
                    value_font_family='googlefont:Raleway',
                    value_font_size=30,
                    value_colors=('white','white','white','white','white','white','white')))     
      for key, value in chart_data.items():
        #self.chart.add(key, value)
        self.chart.add(key, value, formatter=lambda x: '%s' % x)
        
      return self.chart.render(is_unicode=True)  
      
class PollHorizontalBarChart():
  def __init__(self, **kwargs):
      self.chart = pygal.HorizontalBar(**kwargs)
      self.chart.print_values = True
      #self.chart.title = 'You Activity'
        
  def get_data(self, poll_data):
      
      choices = {}
      choices[poll_data.choice1] = (poll_data.choice1stat / poll_data.total) * 100
      choices[poll_data.choice2] = (poll_data.choice2stat / poll_data.total) * 100
      choices[poll_data.choice3] = (poll_data.choice3stat / poll_data.total) * 100
      choices[poll_data.choice4] = (poll_data.choice4stat / poll_data.total) * 100
           
      return choices
  
  def generate(self, poll_data):
      chart_data = self.get_data(poll_data)
      
      print(chart_data)
      
      for key, value in chart_data.items():
        self.chart.add(key, value)
        #self.chart.add(key, value, formatter=lambda x: '%s' % x)
      
      return self.chart.render(is_unicode=True)      