from django.urls import path
from core import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name='index'),
    path('add_product',views.add_product,name='add_product'),
    
    path('product_desc/<pk>',views.product_desc,name="product_desc"),
    
    path('add_to_cart/<pk>',views.add_to_cart,name="add_to_cart"),
    
    path('orderlist',views.orderlist,name="orderlist"),
    
    path('add_item/<int:pk>',views.add_item,name="add_item"),
    
    path('remove_item/<int:pk>',views.remove_item,name="remove_item"),
    
   path('checkout_page',views.checkout_page,name='checkout_page'),
   path("payment",views.payment,name="payment"),
   path('handlerequest',views.handlerequest,name="handlerequest"),
   path('invoice',views.invoice,name='invoice'),
   path('contact_us',views.contact_us,name="contact_us"),
   path('contact_view', views.contact_view, name='contact_view'),
   path('sentmsg/<int:id>',views.sentmsg,name='sentmsg'),
   path('add_category',views.add_category,name="add_category"),
   
   
   path('productview',views.productview,name='productview'),
   path('deletepro/<int:product_id>',views.deletepro,name='deletepro'),
   path('update_product/<int:product_id>',views.update_product,name='update_product'),
   path('order_list/', views.order_list, name='order_list'),
   path('order_li/', views.order_li, name='order_li'),
#    path('render_pdf_view',views.render_pdf_view,name='render_pdf_view'),

    
    
] +  static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

