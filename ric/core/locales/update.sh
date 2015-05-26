domain=ric
#i18ndude rebuild-pot --pot $domain.pot --merge $domain-manual.pot  --create $domain ../
i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po

domain=collective.contact.core
i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po
