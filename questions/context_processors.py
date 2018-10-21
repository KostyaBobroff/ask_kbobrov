

def get_best_users(request):
    best_users = ['kostya', 'polya', 'masha','vovA']
    return {
        'best_users': best_users
    }

def get_best_tags(request):
    best_tags = ['django', 'js', 'IU-6']
    return {"best_tags":best_tags}