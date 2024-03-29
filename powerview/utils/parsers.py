import argparse
import sys
import logging

from impacket import version

def arg_parse():
    parser = argparse.ArgumentParser(description = "Python alternative to SharpSploit's PowerView script")
    parser.add_argument('account', action='store', metavar='[domain/]username[:password]', help='Account used to authenticate to DC.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--use-ldaps', dest='use_ldaps', action='store_true', help='Use LDAPS instead of LDAP')
    group.add_argument('--use-gc', dest='use_gc', action='store_true', help='Use GlobalCatalog (GC) protocol')
    group.add_argument('--use-gc-ldaps', dest='use_gc_ldaps', action='store_true', help='Use GlobalCatalog (GC) protocol for LDAPS')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Enable debug output')

    auth = parser.add_argument_group('authentication')
    auth.add_argument('-H','--hashes', action="store", metavar = "LMHASH:NTHASH", help='NTLM hashes, format is LMHASH:NTHASH')
    auth.add_argument("-k", "--kerberos", dest="use_kerberos", action="store_true", help='Use Kerberos authentication. Grabs credentials from .ccache file (KRB5CCNAME) based on target parameters. If valid credentials cannot be found, it will use the ones specified in the command line')
    auth.add_argument('--no-pass', action="store_true", help="don't ask for password (useful for -k)")
    auth.add_argument('--aes-key', dest="auth_aes_key", action="store", metavar = "hex key", help='AES key to use for Kerberos Authentication \'(128 or 256 bits)\'')
    auth.add_argument("--dc-ip", action='store', metavar='IP address', help='IP Address of the domain controller or KDC (Key Distribution Center) for Kerberos. If omitted it will use the domain part (FQDN) specified in the identity parameter')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
        # Print the Library's installation path
        logging.debug(version.getInstallationPath())
    else:
        logging.getLogger().setLevel(logging.INFO)

    return args

def powerview_arg_parse(cmd):
    parser = argparse.ArgumentParser(exit_on_error=False)
    subparsers = parser.add_subparsers(dest='module')
    parser.add_argument('-Domain', action='store', dest='server')
    parser.add_argument('-Where', action='store', dest='where')
    parser.add_argument('-Select', action='store', dest='select')
    parser.add_argument('-NoWrap', action='store', dest='nowrap')

    #domain
    get_domain_parser = subparsers.add_parser('Get-Domain', aliases=['Get-NetDomain'], exit_on_error=False)
    get_domain_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domain_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domain_parser.add_argument('-Domain', action='store', dest='server')
    get_domain_parser.add_argument('-Select', action='store', dest='select')
    get_domain_parser.add_argument('-Where', action='store', dest='where')
    get_domain_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #domainobject
    get_domainobject_parser = subparsers.add_parser('Get-DomainObject', aliases=['Get-ADObject'] ,exit_on_error=False)
    get_domainobject_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domainobject_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domainobject_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    get_domainobject_parser.add_argument('-Domain', action='store', dest='server')
    get_domainobject_parser.add_argument('-Select', action='store', dest='select')
    get_domainobject_parser.add_argument('-Where', action='store', dest='where')
    get_domainobject_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #domainobjectacl
    get_domainobjectacl_parser = subparsers.add_parser('Get-DomainObjectAcl', aliases=['Get-ObjectAcl'] ,exit_on_error=False)
    get_domainobjectacl_parser.add_argument('-Identity', action='store', default='*', dest='identity')
    get_domainobjectacl_parser.add_argument('-Domain', action='store', dest='server')
    get_domainobjectacl_parser.add_argument('-SecurityIdentifier', action='store', dest='security_identifier')
    get_domainobjectacl_parser.add_argument('-ResolveGUIDs', action='store_true',default=False, dest='resolveguids')
    get_domainobjectacl_parser.add_argument('-Select', action='store', dest='select')
    get_domainobjectacl_parser.add_argument('-Where', action='store', dest='where')
    get_domainobjectacl_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #group
    get_domaingroup_parser = subparsers.add_parser('Get-DomainGroup', aliases=['Get-NetGroup'], exit_on_error=False)
    get_domaingroup_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domaingroup_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domaingroup_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    get_domaingroup_parser.add_argument('-MemberIdentity', action='store', dest='memberidentity')
    get_domaingroup_parser.add_argument('-AdminCount', action='store_true', default=False, dest='admincount')
    get_domaingroup_parser.add_argument('-Domain', action='store', dest='server')
    get_domaingroup_parser.add_argument('-Select', action='store', dest='select')
    get_domaingroup_parser.add_argument('-Where', action='store', dest='where')
    get_domaingroup_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #groupmember
    get_domaingroupmember_parser = subparsers.add_parser('Get-DomainGroupMember', aliases=['Get-NetGroupMember'], exit_on_error=False)
    get_domaingroupmember_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domaingroupmember_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    get_domaingroupmember_parser.add_argument('-Domain', action='store', dest='server')
    get_domaingroupmember_parser.add_argument('-Select', action='store', dest='select')
    get_domaingroupmember_parser.add_argument('-Where', action='store', dest='where')
    get_domaingroupmember_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #user
    get_domainuser_parser = subparsers.add_parser('Get-DomainUser', aliases=['Get-NetUser'], exit_on_error=False)
    get_domainuser_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domainuser_parser.add_argument('-Properties', action='store',default='*', dest='properties')
    get_domainuser_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    get_domainuser_parser.add_argument('-Domain', action='store', dest='server')
    get_domainuser_parser.add_argument('-Select', action='store', dest='select')
    get_domainuser_parser.add_argument('-Where', action='store', dest='where')
    get_domainuser_parser.add_argument('-SPN', action='store_true', default=False, dest='spn')
    get_domainuser_parser.add_argument('-AdminCount', action='store_true', default=False, dest='admincount')
    get_domainuser_parser.add_argument('-PassNotRequired', action='store_true', default=False, dest='passnotrequired')
    get_domainuser_parser.add_argument('-RBCD', action='store_true', default=False, dest='rbcd')
    get_domainuser_parser.add_argument('-PreAuthNotRequired', action='store_true', default=False, dest='preauthnotrequired')
    get_domainuser_parser.add_argument('-TrustedToAuth', action='store_true', default=False, dest='trustedtoauth')
    get_domainuser_parser.add_argument('-AllowDelegation', action='store_true', default=False, dest='allowdelegation')
    get_domainuser_parser.add_argument('-DisallowDelegation', action='store_true', default=False, dest='disallowdelegation')
    get_domainuser_parser.add_argument('-Unconstrained', action='store_true', default=False, dest='unconstrained')
    get_domainuser_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #computers
    get_domaincomputer_parser = subparsers.add_parser('Get-DomainComputer', aliases=['Get-NetComputer'],exit_on_error=False)
    get_domaincomputer_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domaincomputer_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domaincomputer_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    get_domaincomputer_parser.add_argument('-Domain', action='store', dest='server')
    get_domaincomputer_parser.add_argument('-Select', action='store', dest='select')
    get_domaincomputer_parser.add_argument('-Where', action='store', dest='where')
    get_domaincomputer_parser.add_argument('-Unconstrained', action='store_true', default=False, dest='unconstrained')
    get_domaincomputer_parser.add_argument('-TrustedToAuth', action='store_true', default=False, dest='trustedtoauth')
    get_domaincomputer_parser.add_argument('-LAPS', action='store_true', default=False, dest='laps')
    get_domaincomputer_parser.add_argument('-RBCD', action='store_true', default=False, dest='rbcd')
    get_domaincomputer_parser.add_argument('-SPN', action='store', dest='spn')
    get_domaincomputer_parser.add_argument('-Printers', action='store_true', default=False, dest='printers')
    get_domaincomputer_parser.add_argument('-ExcludeDCs', action='store_true', default=False, dest='excludedcs')
    get_domaincomputer_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #domain controller
    get_domaincontroller_parser = subparsers.add_parser('Get-DomainController', aliases=['NetDomainController '], exit_on_error=False)
    get_domaincontroller_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domaincontroller_parser.add_argument('-Properties',action='store',default='*', dest='properties')
    get_domaincontroller_parser.add_argument('-Domain', action='store', dest='server')
    get_domaincontroller_parser.add_argument('-Select',action='store', dest='select')
    get_domaincontroller_parser.add_argument('-Where', action='store', dest='where')
    get_domaincontroller_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #gpo
    get_domaingpo_parser = subparsers.add_parser('Get-DomainGPO', aliases=['Get-NetGPO'], exit_on_error=False)
    get_domaingpo_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domaingpo_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domaingpo_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    get_domaingpo_parser.add_argument('-Domain', action='store', dest='server')
    get_domaingpo_parser.add_argument('-Select', action='store', dest='select')
    get_domaingpo_parser.add_argument('-Where', action='store', dest='where')
    get_domaingpo_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #gpo local group / restricted groups
    get_domaingpolocalgroup_parser = subparsers.add_parser('Get-DomainGPOLocalGroup', aliases=['Get-GPOLocalGroup'], exit_on_error=False)
    get_domaingpolocalgroup_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domaingpolocalgroup_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    get_domaingpolocalgroup_parser.add_argument('-Domain', action='store', dest='server')
    get_domaingpolocalgroup_parser.add_argument('-Select', action='store', dest='select')
    get_domaingpolocalgroup_parser.add_argument('-Where', action='store', dest='where')
    get_domaingpolocalgroup_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    # OU
    get_domainou_parser = subparsers.add_parser('Get-DomainOU', aliases=['Get-NetOU'], exit_on_error=False)
    get_domainou_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domainou_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domainou_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    get_domainou_parser.add_argument('-Domain', action='store', dest='server')
    get_domainou_parser.add_argument('-Select', action='store', dest='select')
    get_domainou_parser.add_argument('-GPLink', action='store', dest='gplink')
    get_domainou_parser.add_argument('-Where', action='store', dest='where')
    get_domainou_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    # Find DNS Zone
    get_domaindns_parser = subparsers.add_parser('Get-DomainDNSZone', exit_on_error=False)
    get_domaindns_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domaindns_parser.add_argument('-Domain', action='store', dest='server')
    get_domaindns_parser.add_argument('-Select', action='store', dest='select')
    get_domaindns_parser.add_argument('-Where', action='store', dest='where')
    get_domaindns_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    # Find CAs
    get_domainca_parser = subparsers.add_parser('Get-DomainCA', aliases=['Get-NetCA'], exit_on_error=False)
    get_domainca_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domainca_parser.add_argument('-Domain', action='store', dest='server')
    get_domainca_parser.add_argument('-Select', action='store', dest='select')
    get_domainca_parser.add_argument('-Where', action='store', dest='where')
    get_domainca_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    # get named pipes
    get_namedpipes_parser = subparsers.add_parser('Get-NamedPipes', exit_on_error=False)
    get_namedpipes_parser.add_argument('-Name', action='store', dest='name')
    get_namedpipes_group = get_namedpipes_parser.add_mutually_exclusive_group()
    get_namedpipes_group.add_argument('-Computer', action='store', const=None, dest='computer')
    get_namedpipes_group.add_argument('-ComputerName', action='store', const=None, dest='computername')
    get_namedpipes_parser.add_argument('-Domain', action='store', dest='server')

    # shares
    get_shares_parser = subparsers.add_parser('Get-Shares', aliases=['Get-NetShares'], exit_on_error=False)
    get_shares_group = get_shares_parser.add_mutually_exclusive_group()
    get_shares_group.add_argument('-Computer', action='store', const=None, dest='computer')
    get_shares_group.add_argument('-ComputerName', action='store', const=None, dest='computername')
    get_shares_parser.add_argument('-Domain', action='store', dest='server')

    # shares
    find_localadminaccess_parser = subparsers.add_parser('Find-LocalAdminAccess', exit_on_error=False)
    find_localadminaccess_parser.add_argument('-Computer', action='store', dest='computer')
    find_localadminaccess_parser.add_argument('-ComputerName', action='store', dest='computername')
    find_localadminaccess_parser.add_argument('-Domain', action='store', dest='server')

    # invoke kerberoast
    invoke_kerberoast_parser = subparsers.add_parser('Invoke-Kerberoast', exit_on_error=False)
    invoke_kerberoast_parser.add_argument('-Identity', action='store', dest='identity')
    invoke_kerberoast_parser.add_argument('-LDAPFilter', action='store', dest='ldapfilter')
    invoke_kerberoast_parser.add_argument('-Domain', action='store', dest='server')
    invoke_kerberoast_parser.add_argument('-Select', action='store', dest='select')
    invoke_kerberoast_parser.add_argument('-Where', action='store', dest='where')
    invoke_kerberoast_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    #trust
    get_domaintrust_parser = subparsers.add_parser('Get-DomainTrust', aliases=['Get-NetTrust'], exit_on_error=False)
    get_domaintrust_parser.add_argument('-Identity', action='store',default='*', dest='identity')
    get_domaintrust_parser.add_argument('-Properties', action='store', default='*', dest='properties')
    get_domaintrust_parser.add_argument('-Domain', action='store', dest='server')
    get_domaintrust_parser.add_argument('-Select', action='store', dest='select')
    get_domaintrust_parser.add_argument('-Where', action='store', dest='where')
    get_domaintrust_parser.add_argument('-NoWrap', action='store_true', default=False, dest='nowrap')

    # convert from sid
    convertfrom_sid_parser = subparsers.add_parser('ConvertFrom-SID' ,exit_on_error=False)
    convertfrom_sid_parser.add_argument('-ObjectSID', action='store', dest='objectsid')
    convertfrom_sid_parser.add_argument('-Domain', action='store', dest='server')

    # add domain group members
    add_domaingroupmember_parser = subparsers.add_parser('Add-DomainGroupMember',aliases=['Add-GroupMember'], exit_on_error=False)
    add_domaingroupmember_parser.add_argument('-Identity', action='store', const=None, dest='identity')
    add_domaingroupmember_parser.add_argument('-Members', action='store', const=None, dest='members')
    add_domaingroupmember_parser.add_argument('-Domain', action='store', dest='server')

    # remove domain group members
    remove_domaingroupmember_parser = subparsers.add_parser('Remove-DomainGroupMember',aliases=['Remove-GroupMember'], exit_on_error=False)
    remove_domaingroupmember_parser.add_argument('-Identity', action='store', const=None, dest='identity')
    remove_domaingroupmember_parser.add_argument('-Members', action='store', const=None, dest='members')
    remove_domaingroupmember_parser.add_argument('-Domain', action='store', dest='server')

    # add domain object acl
    add_domainobjectacl_parser = subparsers.add_parser('Add-DomainObjectAcl', aliases=['Add-ObjectAcl'], exit_on_error=False)
    add_domainobjectacl_parser.add_argument('-TargetIdentity', action='store', const=None, dest='targetidentity')
    add_domainobjectacl_parser.add_argument('-PrincipalIdentity', action='store', const=None, dest='principalidentity')
    add_domainobjectacl_parser.add_argument('-Rights', action='store', const=None, dest='rights', choices=['all', 'dcsync', 'writemembers','resetpassword','rbcd','shadowcred'], type = str.lower)
    add_domainobjectacl_parser.add_argument('-Domain', action='store', dest='server')

    # remove domain object acl
    remove_domainobjectacl_parser = subparsers.add_parser('Remove-DomainObjectAcl', aliases=['Remove-ObjectAcl'], exit_on_error=False)
    remove_domainobjectacl_parser.add_argument('-TargetIdentity', action='store', const=None, dest='targetidentity')
    remove_domainobjectacl_parser.add_argument('-PrincipalIdentity', action='store', const=None, dest='principalidentity')
    remove_domainobjectacl_parser.add_argument('-Rights', action='store', const=None, dest='rights', choices=['all', 'dcsync','writemembers','resetpassword'], type = str.lower)
    remove_domainobjectacl_parser.add_argument('-Domain', action='store', dest='server')

    # add domain computer
    add_domaincomputer_parser = subparsers.add_parser('Add-DomainComputer', aliases=['Add-ADComputer'], exit_on_error=False)
    add_domaincomputer_parser.add_argument('-ComputerName', action='store', const=None, dest='computername')
    add_domaincomputer_parser.add_argument('-ComputerPass', action='store', const=None, dest='computerpass')
    add_domaincomputer_parser.add_argument('-Domain', action='store', dest='server')

    # add domain user
    add_domainuser_parser = subparsers.add_parser('Add-DomainUser', aliases=['Add-ADUser'], exit_on_error=False)
    add_domainuser_parser.add_argument('-UserName', action='store', default=None, const=None, dest='username')
    add_domainuser_parser.add_argument('-UserPass', action='store', default=None, const=None, dest='userpass')
    add_domainuser_parser.add_argument('-Domain', action='store', dest='server')

    # remove domain user
    remove_domainuser_parser = subparsers.add_parser('Remove-DomainUser', aliases=['Remove-ADUser'], exit_on_error=False)
    remove_domainuser_parser.add_argument('-Identity', action='store', dest='identity')
    remove_domainuser_parser.add_argument('-Domain', action='store', dest='server')

    # remove domain computer
    remove_domaincomputer_parser = subparsers.add_parser('Remove-DomainComputer', aliases=['Remove-ADComputer'], exit_on_error=False)
    remove_domaincomputer_parser.add_argument('-ComputerName',action='store', const=None, dest='computername')
    remove_domaincomputer_parser.add_argument('-Domain', action='store', dest='server')

    # set domain object properties
    set_domainobject_parser = subparsers.add_parser('Set-DomainObject', aliases=['Set-ADObject'], exit_on_error=False)
    set_domainobject_parser.add_argument('-Identity', action='store', dest='identity')
    set_domainobject_parser.add_argument('-Set', dest='set')
    set_domainobject_parser.add_argument('-Clear',action='store', dest='clear')
    set_domainobject_parser.add_argument('-Domain', action='store', dest='server')

    # set domain object properties
    set_domainuserpassword_parser = subparsers.add_parser('Set-DomainUserPassword', exit_on_error=False)
    set_domainuserpassword_parser.add_argument('-identity', '-Identity', action='store', dest='identity')
    set_domainuserpassword_parser.add_argument('-accountpassword', '-AccountPassword', action='store', dest='accountpassword')
    set_domainuserpassword_parser.add_argument('-domain', '-Domain', action='store', dest='server')

    subparsers.add_parser('exit', exit_on_error=False)
    subparsers.add_parser('clear', exit_on_error=False)

    try:
        args, unknown = parser.parse_known_args(cmd)
        if unknown:
            for unk in unknown:
                if unk[0] == "-":
                    if unk.casefold() in [ item.casefold() for item in COMMANDS[cmd[0]] ] :
                        indexs = [item.lower() for item in COMMANDS[cmd[0]]].index(unk.lower())
                        cmd = [c.replace(unk,COMMANDS[cmd[0]][indexs]) for c in cmd]
                    else:
                        logging.error(f"Unrecognized argument: {unk}")
                        return None
            return parser.parse_args(cmd)
        return args
    except argparse.ArgumentError as e:
        for i in list(COMMANDS.keys()):
            if cmd[0].casefold() == i.casefold():
                cmd[0] = i
                return parser.parse_args(cmd)

        logging.error(str(e).split("(")[0])
        return None
