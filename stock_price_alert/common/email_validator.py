from disposable_email_checker.emails import email_domain_loader


def custom_email_domain_loader():
    # Anyone still using AOL will be too much of a customer service burden
    return [
        "aol.com",
        "yahoo.com",
    ] + email_domain_loader()
