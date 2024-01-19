from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, OrderItem, Order, Payment, Favorite
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from accounts.models import CustomUser
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import SearchForm
import stripe

class IndexView(ListView):
    model = Item
    template_name = 'app/index.html'
    context_object_name = 'items'
    form_class = SearchForm

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Item.objects.filter(category__name__icontains=query)
        else:
            return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'app/product.html'

    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.object.category.all()
        return context


class ThanksView(LoginRequiredMixin, TemplateView):
    template_name = 'app/thanks.html'


class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order': order
            }
            return render(request, 'app/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/order.html')


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user_data = CustomUser.objects.get(id=request.user.id)
        context = {
            'order': order,
            'user_data': user_data
        }
        return render(request, 'app/payment.html', context)

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = Order.objects.get(user=request.user, ordered=False)
        token = request.POST.get('stripeToken')

        amount = int(round(order.get_total() * 100))
        order_items = order.items.all()
        item_list = []
        for order_item in order_items:
            item_list.append(str(order_item.item) + ':' + str(order_item.quantity))
        description = ' '.join(item_list)

        charge = stripe.Charge.create(
            amount=amount,
            currency='brl',
            description=description,
            source=token,
        )

        payment = Payment(user=request.user)
        payment.stripe_charge_id = charge['id']
        payment.amount = amount
        payment.save()

        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        order.payment = payment
        order.save()

        subject = 'Thank you for your purchase!'
        email_message = 'Thank you for the purchase. Here are your logos. \n\n LOGOEN'
        email = EmailMessage(subject, email_message, to=[request.user.email])

        for order_item in order_items:
            image_path = order_item.item.image.path
            email.attach_file(image_path)

        email.send()

        return redirect('thanks')
    



@login_required
def addItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order = Order.objects.filter(user=request.user, ordered=False)

    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)

    return redirect('order')


@login_required
def removeItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            return redirect("order")

    return redirect("product", slug=slug)


@login_required
def removeSingleItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            return redirect("order")

    return redirect("product", slug=slug)


class FavoriteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            favorites = Favorite.objects.filter(user=request.user)
            context = {
                'favorites': favorites
            }
            return render(request, 'app/favorited.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/favorited.html')


@login_required
def favorite(request, slug):
    item = get_object_or_404(Item, slug=slug)
    favorite, created = Favorite.objects.get_or_create(
        item=item,
        user=request.user,
    )
    if not created:
        favorite.delete()

        return redirect('favorited')
    
    return redirect('product', slug=item.slug)
