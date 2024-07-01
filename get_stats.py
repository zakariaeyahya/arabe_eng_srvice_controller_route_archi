def get_stats(data_list):
    total_requests = len(data_list)
    languages_used = set()
    for item in data_list:
        languages_used.add(item.get('src_lang', ''))
        languages_used.add(item.get('tgt_lang', ''))
    languages_used.discard('')
    return {
        "total_requests": total_requests,
        "languages_used": list(languages_used)
    }