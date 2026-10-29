from app.dto.user import UserBaseFilter
from app.repositories.user import UserQueryFilter
from app.utils.common import split_to_int_list


def mapping_user_base_filter(filter: UserBaseFilter) -> UserQueryFilter:
    new_filter = UserQueryFilter()

    if filter.roles:
        new_filter.roles = split_to_int_list(filter.roles)

    if filter.search:
        new_filter.search = filter.search

    return new_filter
