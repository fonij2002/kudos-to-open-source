# Virtualization

| Proprietary / licensed product | Open-source alternative | Runs on | Install / use | Things to know | Notes |
|---|---|---|---|---|---|---|---|
| Citrix Hypervisor | [XCP-ng](https://github.com/xcp-ng/xcp) | Linux server | [Install / use](https://docs.xcp-ng.org/installation/install-xcp-ng/) | Usually needs a dedicated host; Linux only | Virtualization platform based on Xen. |
| VMware vSphere | [Proxmox VE](https://www.proxmox.com/en/proxmox-virtual-environment/overview) | Linux server | [Install / use](https://www.proxmox.com/en/downloads) | Usually needs a dedicated host; Linux only | Virtualization platform based on KVM/LXC. |
| VMware Workstation | [QEMU](https://gitlab.com/qemu-project/qemu) | Windows, macOS, Linux | [Install / use](https://www.qemu.org/download/) | Steeper learning curve; CLI-first workflow | Machine emulation and virtualization. |
| VMware Workstation | [virt-manager](https://github.com/virt-manager/virt-manager) | Linux | [Install / use](https://virt-manager.org/download/) | Linux only | Desktop UI for libvirt/QEMU/KVM. |

[← Back to the main catalog](../../README.md)
