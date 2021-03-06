*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test organization editable by members
    Log in  tintin  secret
    # Organization must be editable by this organization members
    Go to  ${PLONE_URL}/annuaire/affinitic
    Wait until page contains  Affinitic
    Element should be visible  css=li#contentview-folderContents a

    # Organization must not be editable by other organizations members
    Go to  ${PLONE_URL}/annuaire/imio
    Wait until page contains  Imio
    Element should not be visible  css=li#contentview-folderContents a


Test invalidmail only editable by admin and visible in view by user
    Log in  tintin  secret
    Go to  ${PLONE_URL}/annuaire/affinitic/tintin/edit
    Wait until page contains  Tin Tin
    Page should not contain  E-mail invalide

    Go to  ${PLONE_URL}/annuaire/affinitic/haddock/edit
    Wait until page contains  Haddock
    Page should not contain  E-mail invalide

    Go to  ${PLONE_URL}
    Log out
    Log in as site owner
    Go to  ${PLONE_URL}/annuaire/affinitic/tintin/edit
    Wait until page contains  Tin Tin
    Page should contain  E-mail invalide


Test invalidmail visible in view by specific user
    Log in  tintin  secret
    Go to  ${PLONE_URL}/annuaire/affinitic/tintin
    Wait until page contains  E-mail invalide  10

    Go to  ${PLONE_URL}/annuaire/affinitic/haddock
    Wait until page contains  haddock  10
    Page should not contain  E-mail invalide


Test userid must be visible only by admin
    Log in  tintin  secret
    Go to  ${PLONE_URL}/annuaire/affinitic/tintin
    Wait until page contains  Tin Tin
    Page should not contain  Identifiant de l'utilisateur 

    Go to  ${PLONE_URL}
    Log out
    Log in as site owner
    Go to  ${PLONE_URL}/annuaire/affinitic/tintin
    Wait until page contains  Tin Tin
    Page should contain  Identifiant de l'utilisateur 


Test userid must be editable only by admin
    Log in  tintin  secret
    Go to  ${PLONE_URL}/annuaire/affinitic/tintin/edit
    Wait until page contains  Tin Tin
    Page should not contain  Identifiant de l'utilisateur 

    Go to  ${PLONE_URL}
    Log out
    Log in as site owner
    Go to  ${PLONE_URL}/annuaire/affinitic/tintin/edit
    Wait until page contains  Tin Tin
    Page should contain  Identifiant de l'utilisateur 


Test subscription must be editable only by admin
    Log in  tintin  secret
    Go to  ${PLONE_URL}/annuaire/affinitic/edit
    Wait until page contains  Affinitic
    Page should not contain  Cotisations

    Go to  ${PLONE_URL}
    Log out
    Log in as site owner
    Go to  ${PLONE_URL}/annuaire/affinitic/edit
    Wait until page contains  Affinitic
    Page should contain  Cotisations


Test subscription must be visible only by admin and organization members
    Log in  tintin  secret
    Go to  ${PLONE_URL}/annuaire/affinitic
    Wait until page contains  Affinitic
    Page should contain  Cotisations

    Go to  ${PLONE_URL}
    Log out
    Log in as site owner
    Go to  ${PLONE_URL}/annuaire/affinitic
    Wait until page contains  Affinitic
    Page should contain  Cotisations

    Go to  ${PLONE_URL}
    Log out
    Log in  dupont  secret
    Go to  ${PLONE_URL}/annuaire/affinitic
    Wait until page contains  Affinitic
    Page should not contain  Cotisations
