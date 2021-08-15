from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from eshop.models import (
    Course,
    Category,
    Slider,
    OffCourse,
)


# Create your views here.


class MainPage(ListView):
    template_name = 'main/index.html'

    def get_queryset(self):
        return Course.objects.order_by('?').filter(active=True)[:12]

    def get_context_data(self, *args, **kwargs):
        context = super(MainPage, self).get_context_data(*args, **kwargs)

        context['category_object_list'] = Category.objects.filter(active=True)
        context['new_object_list'] = Course.objects.filter(
            active=True).order_by('-publish')[:8]
        context['slider_object_list'] = Slider.objects.filter(active=True)[:3]
        context['discount'] = OffCourse.objects.filter(active=True)
        return context


class DetailPage(DetailView):
    template_name = 'main/product-detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Course, active=True, slug=slug)

    def get_context_data(self, *args, **kwargs):
        context = super(DetailPage, self).get_context_data(*args, **kwargs)
        context['discount'] = OffCourse.objects.filter(active=True).first()
        return context


class VideoViewPage(LoginRequiredMixin, DetailView):
    template_name = 'main/video_viewer.html'
    login_url = 'account:login'

    def get(self, request, slug, file_id):
        course = get_object_or_404(Course, active=True, slug=slug)
        for cart in self.request.user.cart_set.filter(is_paid=True):
            for sub_cart in cart.subcart_set.all():
                if sub_cart.course == course:
                    return render(request, self.template_name, {'object': course.files.get(id=file_id)})
        return redirect('main:detail', slug=course.slug)


class CategoryViewPage(ListView):
    template_name = 'main/shop-grid-full.html'

    def get_queryset(self):
        global category_slug
        category_slug = self.kwargs.get('slug')
        if category_slug == 'all':
            return Course.objects.filter(active=True).order_by('-publish')
        else:
            return Course.objects.filter(active=True, category__slug=category_slug)

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryViewPage, self).get_context_data(
            *args, **kwargs)
        try:
            context['category'] = get_object_or_404(
                Category, active=True, slug=category_slug)
        except:
            context['category'] = 'همه'
        return context

class DashboardView(LoginRequiredMixin, View):
    template_name = './accounts/dashboard.html'
    login_url = 'account:login'

    def get(self, request):
        paid_carts = request.user.cart_set.filter(is_paid=True)

        context = {
            "paid_carts_count": paid_carts.count(),
            "paid_carts": paid_carts,
            "paid_courses": [ [ subcart.course for subcart in carts.subcart_set.all() ] for carts in paid_carts] 
        }
        return render(request, self.template_name, context)

