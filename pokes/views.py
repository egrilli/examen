from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from pokes.models import User
from pokes.decorators import *


def vacio(request):
    return redirect ("/main")

def index(request):
    return render(request, 'index.html')


def registro(request):
    if request.method == "POST":
        errors = User.objects.validador_basico(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            request.session['registro_nombre'] =  request.POST['firstname']
            request.session['registro_alias'] =  request.POST['alias']
            request.session['registro_email'] =  request.POST['email']

        else:
            request.session['registro_nombre'] = ""
            request.session['registro_alias'] = ""
            request.session['registro_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                firstname = request.POST['firstname'],
                alias=request.POST['alias'],
                email=request.POST['email'],
                password=password_encryp,
                birthday = request.POST['birthday']
            )

            messages.success(request, "El usuario fue agregado con exito.")
            
        return redirect("/")
    else:
        return render(request, 'index.html')


def logearse(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                usuario = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "email": log_user.email,
                }

                request.session['usuario'] = usuario
                messages.success(request, "Logeado correctamente.")
                return redirect("/pokes")
            else:
                messages.error(request, "Password o Email  malas.")
        else:
            messages.error(request, "Email o password malas.")

        return redirect("/logearse")
    else:
        return render(request, 'index.html')

    return render(request, 'index.html')



@login_required
def pokes(request):

    Usuario = User.objects.get(id= request.session['usuario']['id'])

    Usuario_Like = Usuario.likes.all()

    context = {
        "Users": User.objects.exclude(id= request.session['usuario']['id']),
        "UsuarioActual": Usuario,
        "Usuario_Like" : Usuario_Like
    }
    return render(request, 'pokes.html', context)


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        messages.error(request, "Sesion Cerrada")
    return redirect("/")

def pokeLike(request,id):

    usuario = User.objects.get(id= request.session['usuario']['id'])
    usuario.likeDado = (int(usuario.likeDado) + 1)
    usuario.save()

    usuario_like = User.objects.get(id=id)
    usuario_like.likeRecibido = (int(usuario_like.likeRecibido) + 1)
    usuario_like.save()

    usuario.megusta.add(usuario_like)




    return redirect("/pokes")



