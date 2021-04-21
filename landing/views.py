from django.shortcuts import render

from pictures.slack import try_slack_message


def home(request):
    try_slack_message("누군가가 홈페이지로 접속했습니다. - 디테일컷 리뉴얼")
    return render(request, 'landingHome.html')


def model_cut_try(request):
    # try_slack_message("누군가가 착용샷 변경 페이지로 이동했습니다.")
    return render(request, 'register_model.html')


def detail_cut_try(request):
    # try_slack_message("누군가가 디테일컷 변경 페이지로 이동했습니다.")
    return render(request, 'register_detail.html')


def select(request):
    # try_slack_message("누군가가 선택 페이지로 이동했습니다.")
    return render(request, 'select.html')


def success(request):
    return render(request, 'success.html')
