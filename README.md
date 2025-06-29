# LinPyMem

Read physical memory from user-space using a kernel-mode driver (`linpmem.ko`) and virtual-to-physical address translation with CR3 walking.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🔍 What is LinPyMem?

LinPyMem is a Python wrapper around the [linpmem](https://github.com/Velocidex/Linpmem) kernel module, enabling:
- Translation of virtual memory addresses to physical addresses
- Reading raw physical memory (primitives, vectors, strings)
- Inspecting memory mapped regions of another Linux process

---

## ⚠️ Requirements

- Linux system with root privileges
- `linpmem.ko` built from source
- Module must be **signed and enrolled via MOK** if **Secure Boot is enabled**
- Python 3.7+
- Dependencies: `psutil`, `ctypes`, `fcntl`, `struct`, `subprocess`

---

## 🔧 Installation

```bash
pip install linpymem
```

## 🔐 Secure Boot Considerations

If Secure Boot is enabled:

  Sign the linpmem.ko using your own key:
  ```bash
  /usr/src/linux-headers-$(uname -r)/scripts/sign-file sha256 MOK.key MOK.crt linpmem.ko
  ```
  
  Enroll the public key:
  ```bash
  sudo mokutil --import MOK.crt
  ```
  
  Reboot and follow the on-screen instructions

## ✅ Usage with context manager (auto-loads and removes driver)
```python
from linpymem import LinPyMem

some_offset = 0xcafebabe
with LinPyMem(ko_module_path="/path/to/linpmem.ko", process_name="firefox", vm_pathname="/usr/lib/x86_64-linux-gnu/libc.so.6") as reader:
    print(f"[+] pid: {reader.pid} vm_range: {hex(reader.process_vm_start_addr)}-{hex(reader.process_vm_end_addr)} size: {hex(reader.process_vm_size)} cr3: {hex(reader.cr3)}")
    regions = reader.pathname_vm_regions
    for base_addr, size in regions:
        data = reader.read_ptr(base_addr + some_offset)
```

## ⚙️ Manual Usage (driver is already loaded and should remain loaded)

```python
from linpymem import LinPyMem, PhysAccessMode

some_offset = 0xcafebabe
reader = LinPyMem(process_name="firefox", vm_pathname="/usr/lib/x86_64-linux-gnu/libc.so.6")
print(f"[+] pid: {reader.pid} vm_range: {hex(reader.process_vm_start_addr)}-{hex(reader.process_vm_end_addr)} size: {hex(reader.process_vm_size)} cr3: {hex(reader.cr3)}")
for base_addr, size in regions:
    # using conveinience function
    data = reader.read_bytes(base_addr + some_offset, 0x1337)

    # or equivalently
    physical_address, pte_virt_addr = reader.virtual_to_physical(base_addr + some_offset, reader.cr3)
    data, num_bytes_read, num_expected_bytes = reader.read_physical_memory(physical_address, PhysAccessMode.PHYS_BUFFER_READ, 0x1337)
```

## 🧭 Available class properties and functions
```python
reader = LinPyMem(...)
reader.pid
reader.process_vm_start_addr
reader.process_vm_end_addr
reader.process_vm_size
reader.pathname_vm_regions # only set when vm_pathname is provided in constuctor
reader.cr3

# optional driver setup/teardown helpers
def insert_kernel_module(self, module_path: str):
def get_driver_major_number(self, driver_name: str) -> int:
def create_device_node(self, major_number: int, device_path: str):
def setup_driver(self, module_path: str, device_path: str):
def remove_driver(self, device_path: str):

# process inspection helpers
def get_pid_by_process_name(self, process_name: str) -> int:
def get_process_virtual_memory_bounds(self, pid: int) -> tuple[int, int, int]:
def get_pathname_virtual_address_range(self, pid: int, pathname: str) -> list[tuple[int, int]]:

# linpmem kernel IOCTL calls
def read_physical_memory(self, phys_addr: int, mode: PhysAccessMode, readbuffer_size: int = 0) -> tuple:
def virtual_to_physical(self, virt_addr: int, cr3: int = 0) -> tuple[int, int]:
def get_cr3_for_process(self, pid: int) -> int:

# convenince functions (constructed with IOCTL primitaves above)
def read_bytes(self, addr: int, size: int) -> bytes:
def read_ptr(self, addr: int) -> int:
def read_short(self, addr: int) -> int:
def read_int(self, addr: int) -> int:
def read_float(self, addr: int) -> float:
def read_double(self, addr: int) -> float:
def read_vec3_float(self, addr: int) -> tuple[float, float, float]:
def read_vec3_double(self, addr: int) -> tuple[float, float, float]:
def read_utf_string(self, addr: int, max_len: int = 1024) -> str:
def view_memory_region(self, start_address: int, size: int, row_size: int = 16):
```
