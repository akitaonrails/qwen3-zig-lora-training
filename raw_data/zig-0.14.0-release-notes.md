[](https://ziglang.org/)

# 0.14.0 Release Notes

![Zero the Ziguana](https://ziglang.org/img/Zero_1.svg)

[Download & Documentation](https://ziglang.org/download/#release-0.14.0)

Zig is a general-purpose programming language and toolchain for maintaining
**robust** , **optimal** , and **reusable** software.

Zig development is funded via [Zig Software Foundation](/zsf/), a 501(c)(3)
non-profit organization. Please consider a recurring donation so that we can
offer more billable hours to our core team members. This is the most
straightforward way to accelerate the project along the Roadmap to 1.0.

This release features **9 months of work** : changes from **251 different
contributors** , spread among **3467 commits**.

Along with a slew of Build System upgrades, Language Changes, and Target
Support enhancements, this release strides towards two of our long-term
investments - Incremental Compilation and fast x86 Backend \- both focused on
**reducing edit/compile/debug cycle latency**.

## Table of Contents §

  * Table of Contents
  * Target Support
    * Target Triple Changes
    * Tier System
      * Tier 1
      * Tier 2
      * Tier 3
      * Tier 4
    * Support Table
    * Additional Platforms
  * Language Changes
    * Labeled Switch
      * Code Generation Properties
    * Decl Literals
      * Fields and Declarations Cannot Share Names
    * @splat Supports Arrays
    * Global Variables can be Initialized with Address of Each Other
    * @export Operand is Now a Pointer
    * New @branchHint Builtin, Replacing @setCold
    * Removal of @fence
      * StoreLoad Barriers
      * Conditional Barriers
      * Synchronize External Operations
    * Packed Struct Equality
    * Packed Struct Atomics
    * @ptrCast Allows Changing Slice Length
    * Remove Anonymous Struct Types, Unify Tuples
    * Calling Convention Enhancements and @setAlignStack Replaced
    * std.builtin.Type Fields Renamed
    * std.builtin.Type.Pointer.Size Field Renamed
    * Simplify Usage Of ?*const anyopaque In std.builtin.Type
    * Non-Scalar Sentinel Types Disallowed
    * @FieldType builtin
    * @src Gains Module Field
    * @memcpy Rules Adjusted
    * Unsafe In-Memory Coercions Disallowed
    * callconv, align, addrspace, linksection Cannot Reference Function Arguments
    * Branch Quota Rules Adjusted for Function Calls
  * Standard Library
    * DebugAllocator
    * SmpAllocator
    * Allocator API Changes (remap)
    * ZON Parsing and Serialization
    * Runtime Page Size
    * Panic Interface
    * Transport Layer Security (std.crypto.tls)
    * process.Child.collectOutput API Changed
    * LLVM Builder API
    * Embracing "Unmanaged"-Style Containers
    * List of Deprecations
    * std.c Reorganization
    * Binary Search
    * std.hash_map gains a rehash method
  * Build System
    * File System Watching
    * New Package Hash Format
    * WriteFile Step
    * RemoveDir Step
    * Fmt Step
    * Creating Artifacts from Existing Modules
    * Allow Packages to Expose Arbitrary LazyPaths by Name
    * addLibrary Function
  * Compiler
    * Multithreaded Backend Support
    * Incremental Compilation
    * x86 Backend
    * Import ZON
    * tokenizer: simplification and spec conformance
    * Include Error Trace in All Functions
  * Linker
    * Move Input File Parsing to the Frontend
    * Wasm Linker Rewritten
  * Fuzzer
  * Bug Fixes
    * This Release Contains Bugs
  * Toolchain
    * UBSan Runtime
    * compiler_rt
      * Optimized memcpy
    * LLVM 19
    * musl 1.2.5
    * glibc 2.41
    * Linux 6.13.4 Headers
    * Darwin libSystem 15.1
    * MinGW-w64
    * wasi-libc
  * Roadmap
  * Thank You Contributors!
  * Thank You Sponsors!

## Target Support §

A major theme in this Zig release is improved target support; the list of
targets that Zig can correctly cross-compile to and run on has been greatly
expanded. The Support Table and Additional Platforms sections cover the
targets that Zig can build programs for, while the [zig-bootstrap
README](https://github.com/ziglang/zig-
bootstrap/blob/master/README.md#supported-triples) covers the targets that the
Zig compiler itself can be easily cross-compiled to run on.

The full list of target-specific fixes is too long to list here, but in short,
if you've ever tried to target arm/thumb, mips/mips64, powerpc/powerpc64,
riscv32/riscv64, or s390x and run into toolchain problems, missing standard
library support, or seemingly nonsensical crashes, then there's a good chance
you'll find that things will Just Work with Zig 0.14.0.

### Target Triple Changes §

Some changes have been made to the target triples understood by Zig:

  * `arm-windows-gnu` has been replaced with `thumb-windows-gnu` to reflect the fact that Windows only supports Thumb-2 mode. 
  * `armeb-windows-gnu` and `aarch64_be-windows-gnu` have been removed as Windows does not support big endian. 
  * `thumb[eb]-linux-musleabi[hf]` have been added for targeting pure Thumb mode using musl libc. 
  * `mips[el]-linux-musleabi` have been added for targeting 32-bit mips with soft float ABI and musl libc. 
  * `mips[el]-linux-musl` have been renamed to `mips[el]-linux-musleabihf` to make it clear that they target hard float ABI. 
  * `mips64[el]-linux-musl` have been renamed to `mips64[el]-linux-muslabi64` to be in line with `mips64[el]-linux-gnuabi64`. 
  * `mips64[el]-linux-muslabin32` have been added to target 64-bit mips with 32-bit pointers and musl libc. 
  * `powerpc-linux-musleabi` has been added for targeting 32-bit powerpc with soft float ABI and musl libc. 
  * `powerpc-linux-musl` has been renamed to `powerpc-linux-musleabihf` to make it clear that this targets hard float ABI. 
  * `x86_64-linux-muslx32` has been added for targeting 64-bit x86 with 32-bit pointers and musl libc. 

### Tier System §

Zig's level of support for various targets is broadly categorized into four
tiers with Tier 1 being the highest. Note that, currently, even some Tier 1
targets may have a few disabled tests as we work towards 100% test pass rate.

#### Tier 1 §

  * All non-experimental language features are known to work correctly. 
  * The compiler can generate machine code for this target without relying on LLVM, while being comparable to LLVM in terms of feature support. 
  * libc is available for this target even when cross-compiling. 

#### Tier 2 §

  * The standard library's cross-platform abstractions have implementations for this target. 
  * This target has debug info capabilities and therefore produces stack traces on failed assertions and crashes. 
  * The CI machines automatically build and test this target on every commit to the `master` branch. 

#### Tier 3 §

  * The compiler can generate machine code for this target by relying on an external backend such as LLVM. 
  * The linker can produce object files, libraries, and executables for this target. 

#### Tier 4 §

  * The compiler can generate assembly source code for this target by relying on an external backend such as LLVM. 
  * This target may be considered experimental by LLVM, in which case it is necessary to build LLVM and Zig from source to be able to use it. 

### Support Table §

In the following table, 🟢 indicates full support, 🔴 indicates no support, and
🟡 indicates that there is partial support, e.g. only for some sub-targets, or
with some notable known issues. ❔ indicates that the status is largely
unknown, typically because the target is rarely exercised. Hover over other
icons for details.

Target | Tier | Lang. Feat. | Std. Lib. | Code Gen. | Linker | Debug Info | libc | CI  
---|---|---|---|---|---|---|---|---  
`x86_64-linux` | [1](https://github.com/ziglang/zig/issues/23079) | 🟢 | 🟢 | 🖥️⚡ | 🟢 | 🟢 | 🟢 | 🟢  
  
* * *  
  
`aarch64[_be]-linux` | [2](https://github.com/ziglang/zig/issues/2443) | 🟢 | 🟢 | 🖥️🛠️ | 🟢 | 🟢 | 🟢 | 🟢  
`aarch64-macos` | [2](https://github.com/ziglang/zig/issues/23078) | 🟢 | 🟢 | 🖥️ | 🟢 | 🟢 | 🟢 | 🟢  
`aarch64-windows` | [2](https://github.com/ziglang/zig/issues/16665) | 🟢 | 🟢 | 🖥️ | 🟢 | 🟢 | 🟢 | 🟢  
`arm[eb]-linux` | [2](https://github.com/ziglang/zig/issues/3174) | 🟢 | 🟢 | 🖥️🛠️ | 🟢 | 🟢 | 🟢 | 🟢  
`powerpc-linux` | [2](https://github.com/ziglang/zig/issues/21649) | 🟢 | 🟢 | 🖥️ | 🟡 | 🟢 | 🟢 | 🟡  
`powerpc64-linux` | [2](https://github.com/ziglang/zig/issues/21651) | 🟢 | 🟢 | 🖥️ | 🟡 | 🟢 | 🟡 | 🟡  
`powerpc64le-linux` | [2](https://github.com/ziglang/zig/issues/21650) | 🟢 | 🟢 | 🖥️ | 🟢 | 🟢 | 🟢 | 🟢  
`wasm32-wasi` | [2](https://github.com/ziglang/zig/issues/23091) | 🟢 | 🟢 | 🖥️⚡ | 🟢 | 🟢 | 🟢 | 🟢  
`x86-linux` | [2](https://github.com/ziglang/zig/issues/1929) | 🟢 | 🟢 | 🖥️ | 🟢 | 🟢 | 🟢 | 🟢  
`x86-windows` | [2](https://github.com/ziglang/zig/issues/537) | 🟢 | 🟢 | 🖥️ | 🟢 | 🟢 | 🟢 | 🟢  
`x86_64-macos` | [2](https://github.com/ziglang/zig/issues/4897) | 🟢 | 🟢 | 🖥️ | 🟢 | 🟢 | 🟢 | 🟢  
`x86_64-windows` | [2](https://github.com/ziglang/zig/issues/23080) | 🟢 | 🟢 | 🖥️ | 🟢 | 🟢 | 🟢 | 🟢  
  
* * *  
  
`aarch64-freebsd` | [3](https://github.com/ziglang/zig/issues/3939) | ❔ | ❔ | 🖥️🛠️ | 🟢 | 🟢 | 🔴 | 🔴  
`aarch64[_be]-netbsd` | [3](https://github.com/ziglang/zig/issues/23084) | ❔ | ❔ | 🖥️🛠️ | 🟢 | ❔ | 🔴 | 🔴  
`aarch64-openbsd` | [3](https://github.com/ziglang/zig/issues/23085) | ❔ | ❔ | 🖥️🛠️ | 🟢 | ❔ | 🔴 | 🔴  
`hexagon-linux` | [3](https://github.com/ziglang/zig/issues/21652) | 🟡 | 🟡 | 🖥️ | 🟢 | 🔴 | 🔴 | 🔴  
`loongarch64-linux` | [3](https://github.com/ziglang/zig/issues/21646) | 🟡 | 🟡 | 🖥️ | 🟢 | 🔴 | 🟢 | 🔴  
`mips[el]-linux` | [3](https://github.com/ziglang/zig/issues/3345) | 🟢 | 🟢 | 🖥️ | 🟢 | 🔴 | 🟢 | 🔴  
`mips64[el]-linux` | [3](https://github.com/ziglang/zig/issues/21647) | 🟢 | 🟢 | 🖥️ | 🟡 | 🔴 | 🟢 | 🔴  
`riscv32-linux` | [3](https://github.com/ziglang/zig/issues/21648) | 🟢 | 🟢 | 🖥️ | 🟢 | 🔴 | 🟢 | 🟢  
`riscv64-linux` | [3](https://github.com/ziglang/zig/issues/4456) | 🟢 | 🟢 | 🖥️🛠️ | 🟢 | 🔴 | 🟢 | 🟢  
`s390x-linux` | [3](https://github.com/ziglang/zig/issues/21402) | 🟢 | 🟢 | 🖥️ | 🟢 | 🔴 | 🟢 | 🟢  
`sparc64-linux` | [3](https://github.com/ziglang/zig/issues/4931) | ❔ | 🟢 | 🖥️🛠️ | 🟢 | ❔ | 🟢 | 🔴  
`sparc64-solaris` | [3](https://github.com/ziglang/zig/issues/23093) | ❔ | ❔ | 🖥️🛠️ | 🟢 | ❔ | 🔴 | 🔴  
`wasm64-wasi` | [3](https://github.com/ziglang/zig/issues/23092) | ❔ | ❔ | 🖥️⚡ | 🟢 | ❔ | 🔴 | 🔴  
`x86_64-dragonfly` | [3](https://github.com/ziglang/zig/issues/7149) | 🟢 | ❔ | 🖥️⚡ | 🟢 | ❔ | 🔴 | 🔴  
`x86_64-freebsd` | [3](https://github.com/ziglang/zig/issues/1759) | 🟢 | 🟢 | 🖥️⚡ | 🟢 | 🟢 | 🔴 | 🔴  
`x86_64-illumos` | [3](https://github.com/ziglang/zig/issues/7152) | 🟢 | ❔ | 🖥️⚡ | 🟢 | ❔ | 🔴 | 🔴  
`x86_64-netbsd` | [3](https://github.com/ziglang/zig/issues/23082) | 🟢 | 🟢 | 🖥️⚡ | 🟢 | 🟢 | 🔴 | 🔴  
`x86_64-openbsd` | [3](https://github.com/ziglang/zig/issues/2016) | 🟢 | 🟢 | 🖥️⚡ | 🟢 | 🟢 | 🔴 | 🔴  
`x86_64-solaris` | [3](https://github.com/ziglang/zig/issues/7151) | 🟢 | ❔ | 🖥️⚡ | 🟢 | ❔ | 🔴 | 🔴  
  
* * *  
  
`arc-linux` | [4](https://github.com/ziglang/zig/issues/23086) | ❔ | 🟢 | 📄 | 🔴 | ❔ | 🟢 | 🔴  
`csky-linux` | [4](https://github.com/ziglang/zig/issues/23087) | ❔ | 🟢 | 📄 | 🔴 | ❔ | 🟢 | 🔴  
`m68k-linux` | [4](https://github.com/ziglang/zig/issues/23089) | ❔ | 🔴 | 🖥️ | 🔴 | ❔ | 🟢 | 🔴  
`m68k-netbsd` | [4](https://github.com/ziglang/zig/issues/23090) | ❔ | 🔴 | 🖥️ | 🔴 | ❔ | 🔴 | 🔴  
`sparc-linux` | [4](https://github.com/ziglang/zig/issues/23081) | ❔ | 🔴 | 🖥️ | 🔴 | ❔ | 🟢 | 🔴  
`xtensa-linux` | [4](https://github.com/ziglang/zig/issues/23088) | ❔ | 🔴 | 📄 | 🔴 | ❔ | 🔴 | 🔴  
  
### Additional Platforms §

Zig also has varying levels of support for these targets, for which the tier
system does not quite apply:

  * `aarch64-driverkit`
  * `aarch64[_be]-freestanding`
  * `aarch64-ios`
  * `aarch64-tvos`
  * `aarch64-uefi`
  * `aarch64-visionos`
  * `aarch64-watchos`
  * `amdgcn-amdhsa`
  * `arc-freestanding`
  * `arm[eb]-freestanding`
  * `avr-freestanding`
  * `bpf(eb,el)-freestanding`
  * `csky-freestanding`
  * `hexagon-freestanding`
  * `kalimba-freestanding`
  * `lanai-freestanding`
  * `loongarch(32,64)-freestanding`
  * `loongarch(32,64)-uefi`
  * `m68k-freestanding`
  * `mips[64][el]-freestanding`
  * `msp430-freestanding`
  * `nvptx[64]-cuda`
  * `nvptx[64]-nvcl`
  * `powerpc[64][le]-freestanding`
  * `propeller-freestanding`
  * `riscv(32,64)-freestanding`
  * `riscv(32,64)-uefi`
  * `s390x-freestanding`
  * `sparc[64]-freestanding`
  * `spirv(32,64)-opencl`
  * `spirv(32,64)-vulkan`
  * `ve-freestanding`
  * `wasm(32,64)-emscripten`
  * `wasm(32,64)-freestanding`
  * `x86-elfiamcu`
  * `x86[_64]-freestanding`
  * `x86[_64]-uefi`
  * `x86_64-driverkit`
  * `x86_64-ios`
  * `x86_64-tvos`
  * `x86_64-visionos`
  * `x86_64-watchos`
  * `xcore-freestanding`
  * `xtensa-freestanding`

## Language Changes §

### Labeled Switch §

Zig 0.14.0 implements [an accepted
proposal](https://github.com/ziglang/zig/issues/8220) which allows `switch`
statements to be labeled, and to be targeted by `continue` statements. Such a
`continue` statement takes a single operand (like `break` can to return a
value from a block or loop); this value is treated as a replacement operand to
the original `switch` expression. This construct is semantically equivalent to
a `switch` statement inside of a loop, with a variable tracking the `switch`
operand; for instance, the following tests are equivalent:

labeled_switch.zig

    
    
    test "labeled switch" {
        foo: switch (@as(u8, 1)) {
            1 => continue :foo 2,
            2 => continue :foo 3,
            3 => return,
            4 => {},
            else => unreachable,
        }
        return error.Unexpected;
    }
    
    test "emulate labeled switch" {
        var op: u8 = 1;
        while (true) {
            switch (op) {
                1 => {
                    op = 2;
                    continue;
                },
                2 => {
                    op = 3;
                    continue;
                },
                3 => return,
                4 => {},
                else => unreachable,
            }
            break;
        }
        return error.Unexpected;
    }

Shell

    
    
    $ zig test labeled_switch.zig
    1/2 labeled_switch.test.labeled switch...OK
    2/2 labeled_switch.test.emulate labeled switch...OK
    All 2 tests passed.
    

These constructs differ in two ways. The most obvious difference is in
clarity: the new syntax form is clearer at times, for instance when
implementing Finite State Automata where one can write `continue :fsa
new_state` to represent a state transition. However, a key motivation for this
language feature lies in its code generation. This is expanded on below.

It is also possible to `break` from a labeled `switch`. This simply terminates
evaluation of the `switch` expression, causing it to result in the given
value, as though the case body were a labeled block. As with blocks, an
unlabeled `break` will never target a `switch` statement; only a `while` or
`for` loop.

Unlike a typical `switch` statement, a labeled `switch` with one or more
`continue`s targeting it is not implicitly evaluated at compile-time (this is
similar to how loops behave). However, as with loops, compile-time evaluation
can be forced by evaluating such an expression in a `comptime` context.

#### Code Generation Properties §

This language construct is designed to generate code which aids the CPU in
predicting branches between cases of the switch, allowing for increased
performance in hot loops, particularly those dispatching instructions,
evaluating FSAs, or performing similar case-based evaluations. To achieve
this, the generated code may be different to what one would intuitively
expect.

If the operand to `continue` is comptime-known, then it can be translated to
an unconditional branch to the relevant case. Such a branch is perfectly
predicted, and hence typically very fast to execute.

If the operand is runtime-known, then each `continue` can become a separate
conditional branch (ideally via a shared jump table) back to the same set of
potential branch targets. The advantage of this pattern is that it aids the
CPU's branch predictor by providing different branch instructions which can be
associated with distinct prediction data. For instance, when evaluating an
FSA, if case `a` is very likely to be followed by case `b`, while case `c` is
very likely to be followed by case `d`, then the branch predictor can use the
direct jumps between `switch` cases to predict the control flow more
accurately, whereas a loop-based lowering causes the state dispatches to be
"collapsed" into a single indirect branch or similar, hindering branch
prediction.

This lowering can inflate code size compared to a simple "switch in a loop"
lowering, and any Zig implementation is, of course, free to lower this syntax
however it wishes provided the language semantics are obeyed. However, the
official ZSF compiler implementation will attempt to match the lowering
described above, particularly in the `ReleaseFast` build mode.

[Updating Zig's tokenizer to take advantage of this feature resulted in a 13%
performance boost](https://github.com/ziglang/zig/pull/21367).

### Decl Literals §

Zig 0.14.0 extends the "enum literal" syntax (`.foo`) to provide a new
feature, known as "decl literals". Now, an enum literal `.foo` doesn't
necessarily refer to an enum variant, but, using [Result Location
Semantics](https://ziglang.org/documentation/0.14.0/#Result-Location-
Semantics), can also refer to any declaration on the target type. For
instance, consider the following example:

decl_literals.zig

    
    
    const S = struct {
        x: u32,
        const default: S = .{ .x = 123 };
    };
    test "decl literal" {
        const val: S = .default;
        try std.testing.expectEqual(123, val.x);
    }
    const std = @import("std");

Shell

    
    
    $ zig test decl_literals.zig
    1/1 decl_literals.test.decl literal...OK
    All 1 tests passed.
    

Since the initialization expression of `val` has a result type of `S`, the
initialization is effectively equivalent to `S.default`. This can be
particularly useful when initializing struct fields to avoid having to specify
the type again:

decl_literals_structs.zig

    
    
    const S = struct {
        x: u32,
        y: u32,
        const default: S = .{ .x = 1, .y = 2 };
        const other: S = .{ .x = 3, .y = 4 };
    };
    const Wrapper = struct {
        val: S = .default,
    };
    test "decl literal initializing struct field" {
        const a: Wrapper = .{};
        try std.testing.expectEqual(1, a.val.x);
        try std.testing.expectEqual(2, a.val.y);
        const b: Wrapper = .{ .val = .other };
        try std.testing.expectEqual(3, b.val.x);
        try std.testing.expectEqual(4, b.val.y);
    }
    const std = @import("std");

Shell

    
    
    $ zig test decl_literals_structs.zig
    1/1 decl_literals_structs.test.decl literal initializing struct field...OK
    All 1 tests passed.
    

It can also help in avoiding [Faulty Default Field
Values](https://ziglang.org/documentation/0.14.0/#Faulty-Default-Field-
Values), like in the following example:

faulty.zig

    
    
    /// `ptr` points to a `[len]u32`.
    pub const BufferA = extern struct { ptr: ?[*]u32 = null, len: usize = 0 };
    // The default values given above are trying to make the buffer default to "empty".
    var empty_buf_a: BufferA = .{};
    // However, they violate the guidance given in the language reference, because you can write this:
    var bad_buf_a: BufferA = .{ .len = 10 };
    // That's not safe, because the `null` and `0` defaults are "tied together". Decl literals make it
    // convenient to represent this case correctly:
    
    /// `ptr` points to a `[len]u32`.
    pub const BufferB = extern struct {
        ptr: ?[*]u32,
        len: usize,
        pub const empty: BufferB = .{ .ptr = null, .len = 0 };
    };
    // We can still easily create an empty buffer:
    var empty_buf_b: BufferB = .empty;
    // ...but the language no longer hides incorrect field overrides from us!
    // If we want to override a field, we'd have to specify both, making the error obvious:
    var bad_buf_b: BufferB = .{ .ptr = null, .len = 10 }; // clearly wrong!

Many existing uses of field default values may be more appropriately handled
by a declaration named `default` or `empty` or similar, to ensure data
invariants are not violated by overriding single fields.

Decl literals also support function calls, like this:

call_decl_literal.zig

    
    
    const S = struct {
        x: u32,
        y: u32,
        fn init(val: u32) S {
            return .{ .x = val + 1, .y = val + 2 };
        }
    };
    test "call decl literal" {
        const a: S = .init(100);
        try std.testing.expectEqual(101, a.x);
        try std.testing.expectEqual(102, a.y);
    }
    const std = @import("std");

Shell

    
    
    $ zig test call_decl_literal.zig
    1/1 call_decl_literal.test.call decl literal...OK
    All 1 tests passed.
    

As before, this syntax can be particularly useful when initializing struct
fields. It also supports calling functions which return error unions via
`try`. The following example uses these in combination to initialize a thin
wrapper around an `ArrayListUnmanaged`:

init_with_decl_literal.zig

    
    
    const Buffer = struct {
        data: std.ArrayListUnmanaged(u32),
        fn initCapacity(allocator: std.mem.Allocator, capacity: usize) !Buffer {
            return .{ .data = try .initCapacity(allocator, capacity) };
        }
    };
    test "initialize Buffer with decl literal" {
        var b: Buffer = try .initCapacity(std.testing.allocator, 5);
        defer b.data.deinit(std.testing.allocator);
        b.data.appendAssumeCapacity(123);
        try std.testing.expectEqual(1, b.data.items.len);
        try std.testing.expectEqual(123, b.data.items[0]);
    }
    const std = @import("std");

Shell

    
    
    $ zig test init_with_decl_literal.zig
    1/1 init_with_decl_literal.test.initialize Buffer with decl literal...OK
    All 1 tests passed.
    

The introduction of decl literals comes with some standard library changes. In
particular, unmanaged containers, including `ArrayListUnmanaged` and
`HashMapUnmanaged`, should no longer be default-initialized with `.{}`,
because the default field values here violate the guidance discussed above.
Instead, they should be initialized using their `empty` declaration, which can
be conveniently accessed via decl literals:

default_init_buffer.zig

    
    
    const Buffer = struct {
        foo: std.ArrayListUnmanaged(u32) = .empty,
    };
    test "default initialize Buffer" {
        var b: Buffer = .{};
        defer b.foo.deinit(std.testing.allocator);
        try b.foo.append(std.testing.allocator, 123);
        try std.testing.expectEqual(1, b.foo.items.len);
        try std.testing.expectEqual(123, b.foo.items[0]);
    }
    const std = @import("std");

Shell

    
    
    $ zig test default_init_buffer.zig
    1/1 default_init_buffer.test.default initialize Buffer...OK
    All 1 tests passed.
    

Similarly, `std.heap.GeneralPurposeAllocator` should now be initialized with
its `.init` declaration.

The deprecated default field values for these data structures will be removed
in the next release cycle.

#### Fields and Declarations Cannot Share Names §

Zig 0.14.0 introduces a restriction that container types (`struct`, `union`,
`enum` and `opaque`) cannot have fields and declarations (`const`/`var`/`fn`)
with the same names. This restriction has been added to deal with the problem
that whether `MyEnum.foo` looks up a declaration or an enum field is ambiguous
(a problem amplified by Decl Literals. Generally, this can be avoided by
following the standard naming conventions:

    
    
    const Foo = struct {
        Thing: Thing,
        const Thing = struct {
            Data: u32,
        };
    };

⬇️

    
    
    const Foo = struct {
        thing: Thing,
        const Thing = struct {
            data: u32,
        };
    };

One upside of this restriction is that documentation comments can now
unambiguously refer to field names, thus enabling such references to be
hyperlinks.

### @splat Supports Arrays §

Zig 0.14.0 expands the `@splat` builtin to apply not only to vectors, but to
arrays. This is useful when default-initializing an array to a constant value.
For instance, in conjunction with Decl Literals, we can elegantly initialize
an array of "color" values:

    
    
    const Rgba = struct {
        r: u8,
        b: u8,
        g: u8,
        a: u8,
        pub const black: Rgba = .{ .r = 0, .g = 0, .b = 0, .a = 255 };
    };
    var pixels: [width][height]Rgba = @splat(@splat(.black));

The operand may be comptime-known or runtime-known. In addition, this builtin
can also be used to initialize sentinel-terminated arrays.

splat.zig

    
    
    const std = @import("std");
    const assert = std.debug.assert;
    const expect = std.testing.expect;
    test "initialize sentinel-terminated array" {
        // the sentinel does not need to match the value
        const arr: [2:0]u8 = @splat(10);
        try expect(arr[0] == 10);
        try expect(arr[1] == 10);
        try expect(arr[2] == 0);
    }
    test "initialize runtime array" {
        var runtime_known: u8 = undefined;
        runtime_known = 123;
        // the operand can be runtime-known, giving a runtime-known array
        const arr: [2]u8 = @splat(runtime_known);
        try expect(arr[0] == 123);
        try expect(arr[1] == 123);
    }
    test "initialize zero-length sentinel-terminated array" {
        var runtime_known: u8 = undefined;
        runtime_known = 123;
        const arr: [0:10]u8 = @splat(runtime_known);
        // the operand was runtime-known, but since the array length was zero, the result is comptime-known
        comptime assert(arr[0] == 10);
    }

Shell

    
    
    $ zig test splat.zig
    1/3 splat.test.initialize sentinel-terminated array...OK
    2/3 splat.test.initialize runtime array...OK
    3/3 splat.test.initialize zero-length sentinel-terminated array...OK
    All 3 tests passed.
    

### Global Variables can be Initialized with Address of Each Other §

This works now:

reference_each_other.zig

    
    
    const std = @import("std");
    const expect = std.testing.expect;
    
    const Node = struct {
        next: *const Node,
    };
    
    const a: Node = .{ .next = &b };
    const b: Node = .{ .next = &a };
    
    test "example" {
        try expect(a.next == &b);
        try expect(b.next == &a);
    }

Shell

    
    
    $ zig test reference_each_other.zig
    1/1 reference_each_other.test.example...OK
    All 1 tests passed.
    

### @export Operand is Now a Pointer §

This release of Zig simplifies the `@export` builtin. In previous versions of
Zig, this builtin's first operand syntactically appeared to be the _value_
which was to be exported, which was restricted to an identifier or field
access of a local variable or container-level declaration. This system was
unnecessarily restrictive, and moreover, syntactically confusing and
inconsistent; it is reasonable to export constant comptime-known values, and
this usage implied that the _value_ was somehow being exported, whereas in
reality its _address_ was the relevant piece of information. To resolve this,
`@export` has a new usage which closely mirrors that of `@extern`; its first
operand is a _pointer_ , which points to the data being exported. In most
cases, solving this will just consist of adding a `&` operator:

    
    
    const foo: u32 = 123;
    test "@export" {
        @export(foo, .{ .name = "bar" });
    }

⬇️

    
    
    const foo: u32 = 123;
    test "@export" {
        @export(&foo, .{ .name = "bar" });
    }

### New @branchHint Builtin, Replacing @setCold §

In high-performance code, it is sometimes desirable to hint to the optimizer
which branch of a condition is more likely; this can allow more efficient
machine code to be generated. Some languages offer this through a "likely"
annotation on a boolean condition; for instance, GCC and Clang implement the
`__builtin_expect` function. Zig 0.14.0 introduces a mechanism to communicate
this information: the new `@branchHint(comptime hint: std.builtin.BranchHint)`
builtin. This builtin, rather than modifying a condition, appears as the first
statement in a block to communicate whether control flow is likely to reach
the block in question:

    
    
    fn warnIf(cond: bool, message: []const u8) void {
        if (cond) {
            @branchHint(.unlikely); // we expect warnings to *not* happen most of the time!
            std.log.warn("{s}", message);
        }
    }
    const std = @import("std");

The `BranchHint` type is as follows:

    
    
    pub const BranchHint = enum(u3) {
        /// Equivalent to no hint given.
        none,
        /// This branch of control flow is more likely to be reached than its peers.
        /// The optimizer should optimize for reaching it.
        likely,
        /// This branch of control flow is less likely to be reached than its peers.
        /// The optimizer should optimize for not reaching it.
        unlikely,
        /// This branch of control flow is unlikely to *ever* be reached.
        /// The optimizer may place it in a different page of memory to optimize other branches.
        cold,
        /// It is difficult to predict whether this branch of control flow will be reached.
        /// The optimizer should avoid branching behavior with expensive mispredictions.
        unpredictable,
    };

As well as being the first statement of a block behind a condition,
`@branchHint` is also permitted as the first statement of any function. The
expectation is that the optimizer may propagate likelihood information to
branches containing these calls; for instance, if a given branch of control
flow always calls a function which is marked `@branchHint(.unlikely)`, then
the optimizer may assume that the branch in question is unlikely to be
reached.

This feature combined with the existence of the `.cold` variant of
`BranchHint` means that the old `@setCold` builtin, which could be used to
communicate that a function is unlikely to ever be called, becomes redundant.
Therefore, `@setCold` has been removed in favor of `@branchHint`. In most
cases, the migration will be very simple; just replace `@setCold(true)` with
`@branchHint(.cold)`:

    
    
    fn foo() void {
        @setCold(true);
        // ...
    }

⬇️

    
    
    fn foo() void {
        @branchHint(.cold);
        // ...
    }

However, remember that `@branchHint` must be the _first statement_ in the
enclosing block, which in this case is the function. This restriction did not
exist for `@setCold`, so non-trivial usages may require small refactors:

    
    
    fn foo(comptime x: u8) void {
        if (x == 0) {
            @setCold(true);
        }
        // ...
    }

⬇️

    
    
    fn foo(comptime x: u8) void {
        @branchHint(if (x == 0) .cold else .none);
        // ...
    }

### Removal of @fence §

In Zig 0.14, `@fence` has been removed. `@fence` was provided to be consistent
with the C11 memory model, however, it complicates semantics by modifying the
memory orderings of all
[previous](https://en.cppreference.com/w/cpp/atomic/atomic_thread_fence#Atomic-
fence_synchronization) and
[future](https://en.cppreference.com/w/cpp/atomic/atomic_thread_fence#Fence-
atomic_synchronization) atomic operations. This creates unforeseen constraints
that are [hard to model in a
sanitizer](https://github.com/google/sanitizers/issues/1415). Fences can be
substituted by either upgrading atomic memory orderings or adding new atomic
operations.

The most common use cases for `@fence` can be replaced by utilizing stronger
memory orderings or by introducing a new atomic variable.

#### StoreLoad Barriers §

The most common use case is `@fence(.seq_cst)`. This is primarily used to
ensure a consistent order between multiple operations on different atomic
variables.

For example:

    
    
    thread-1:                     thread-2:
    store X         // A          store Y          // C
    fence(seq_cst)  // F1         fence(seq_cst)   // F2
    load  Y         // B          load  X          // D
    

The goal is to ensure either `load X` (D) sees `store X` (A), or `load Y` (B)
sees `store Y` (C). The pair of Sequentially Consistent fences guarantees this
via
[two](https://en.cppreference.com/w/cpp/atomic/memory_order#Strongly_happens-
before:~:text=for%20every%20pair%20of%20atomic%20operations%20A%20and%20B%20on%20an%20object%20M%2C%20where%20A%20is%20coherence%2Dordered%2Dbefore%20B%3A)
[invariance](https://en.cppreference.com/w/cpp/atomic/memory_order#Strongly_happens-
before:~:text=if%20a%20memory_order_seq_cst%20fence%20X%20happens%2Dbefore%20A%2C%20and%20B%20happens%2Dbefore%20a%20memory_order_seq_cst%20fence%20Y%2C%20then%20X%20precedes%20Y%20in%20S.).

Now that `@fence` is removed, there are other ways of achieving this
relationship:

  * Making all related stores and loads (A, B, C, and D) `SeqCst`, including them all in the total order.
  * Making a store (A/C) `Acquire` and its matching load (D/B) `Release`. Semantically, this would mean upgrading them to read-modify-write operations, which could be such ordering. Loads can be replaced with a non-mutating RMW, i.e. `fetchAdd(0)` or `fetchOr(0)`.

Optimizers like LLVM may reduce this into a `@fence(.seq_cst) + load`
internally.

#### Conditional Barriers §

Another use case for fences is conditionally creating a _synchronizes-with_
relationship with previous or future atomic operations, using `Acquire` or
`Release` respectively. A simple example of this in the real world is an
atomic reference counter:

sample_code

    
    
    fn inc(counter: *RefCounter) void {
      _ = counter.rc.fetchAdd(1, .monotonic);
    }
    
    fn dec(counter: *RefCounter) void {
      if (counter.rc.fetchSub(1, .release) == 1) {
          @fence(.acquire);
          counter.deinit();
      }
    }

The load in the `fetchSub(1)` only needs to be `Acquire` for the last ref-
count decrement to ensure previous decrements _happen-before_ the `deinit()`.
The `@fence(.acquire)` here creates this relationship using the load part of
the `fetchSub(1)`.

Without `@fence`, there are two approaches here:

  1. Unconditionally strengthen the desired atomic operations with the fence's ordering. sample_code
    
        if (counter.rc.fetchSub(1, .acq_rel) == 1) {

  2. Conditionally duplicate the desired store or load with the fence's ordering sample_code
    
        if (counter.rc.fetchSub(1, .release) == 1) {
        _ = counter.rc.load(.acquire);

The `Acquire` will _synchronize-with_ the longest release-sequence in `rc`'s
modification order, making all previous decrements _happen-before_ the
`deinit()`.

#### Synchronize External Operations §

The least common usage of `@fence` is providing additional synchronization to
atomic operations the programmer has no control over (i.e. external function
calls). Using a `@fence` in this situation relies on the "hidden" functions
having atomic operations with undesirably weak orderings.

Ideally, the "hidden" functions would be accessible to the user and they could
simply increase the order in the source code. But if this isn't possible, a
last resort is introducing an atomic variable to simulate the fence's
barriers. For example:

    
    
    thread-1:                    thread-2:
      queue.push()                e = signal.listen()
      fence(.seq_cst)             fence(.seq_cst)
      signal.notify()             if queue.empty(): e.wait()
    
    
    
    thread-1:                    thread-2:
      queue.push()                e = signal.listen()
      fetchAdd(0, .seq_cst)       fetchAdd(0, .seq_cst)
      signal.notify()             if queue.empty(): e.wait()
    

### Packed Struct Equality §

Packed structs can now be equated directly, without a `@bitCast` to the
underlying integer type.

packed_struct_equality.zig

    
    
    const std = @import("std");
    const expect = std.testing.expect;
    
    test "packed struct equality" {
        const S = packed struct {
            a: u4,
            b: u4,
        };
        const x: S = .{ .a = 1, .b = 2 };
        const y: S = .{ .b = 2, .a = 1 };
        try expect(x == y);
    }

Shell

    
    
    $ zig test packed_struct_equality.zig
    1/1 packed_struct_equality.test.packed struct equality...OK
    All 1 tests passed.
    

### Packed Struct Atomics §

Packed structs can now be used in atomic operations, without a `@bitCast` to
the underlying integer type.

packed_struct_atomics.zig

    
    
    const std = @import("std");
    const expect = std.testing.expect;
    
    test "packed struct atomics" {
        const S = packed struct {
            a: u4,
            b: u4,
        };
        var x: S = .{ .a = 1, .b = 2 };
        const y: S = .{ .a = 3, .b = 4 };
        const prev = @atomicRmw(S, &x, .Xchg, y, .seq_cst);
        try expect(prev.b == 2);
        try expect(x.b == 4);
    }

Shell

    
    
    $ zig test packed_struct_atomics.zig
    1/1 packed_struct_atomics.test.packed struct atomics...OK
    All 1 tests passed.
    

### @ptrCast Allows Changing Slice Length §

[#22706](https://github.com/ziglang/zig/pull/22706)

### Remove Anonymous Struct Types, Unify Tuples §

This change reworks how anonymous struct literals and tuples work.

Previously, an untyped anonymous struct literal (e.g. `const x = .{ .a = 123
}`) was given an "anonymous struct type", which is a special kind of struct
which coerces using structural equivalence. This mechanism was a holdover from
before we used [Result Location
Semantics](https://ziglang.org/documentation/0.14.0/#Result-Location-
Semantics) as the primary mechanism of type inference. This change changes the
language so that the type assigned here is a "normal" struct type. It uses a
form of equivalence based on the AST node and the type's structure, much like
a reified (`@Type`) type.

Additionally, tuples have been simplified. The distinction between "simple"
and "complex" tuple types is eliminated. All tuples, even those explicitly
declared using `struct { ... }` syntax, use structural equivalence, and do not
undergo staged type resolution. Tuples are very restricted: they cannot have
non-`auto` layouts, cannot have aligned fields, and cannot have default values
with the exception of `comptime` fields. Tuples currently do not have
optimized layout, but this can be changed in the future.

This change simplifies the language, and fixes some problematic coercions
through pointers which led to unintuitive behavior.

### Calling Convention Enhancements and @setAlignStack Replaced §

Zig allows setting the calling convention of a function with the
`callconv(...)` annotation, where the value in parentheses is of type
`std.builtin.CallingConvention`. In previous versions of Zig, this type was a
simple `enum` listing a small number of common calling conventions, such as
`.Stdcall` for x86 and `.AAPCS` for ARM. The `.C` variant referred to the
default C calling convention for the target.

Zig 0.14.0 changes `CallingConvention` to be far more exhaustive: it now
contains every major calling convention for every target currently supported
by Zig. Variants have names like `.x86_64_sysv`, `.arm_aapcs`, and
`.riscv64_interrupt`. In addition, instead of an enum, `CallingConvention` is
now a tagged union; this allows _options_ to be specified on a calling
convention.

Most available calling conventions have a payload of
`std.builtin.CallingConvention.CommonOptions`, which allows overriding the
expected alignment of the stack when the function is called:

    
    
    /// Options shared across most calling conventions.
    pub const CommonOptions = struct {
        /// The boundary the stack is aligned to when the function is called.
        /// `null` means the default for this calling convention.
        incoming_stack_alignment: ?u64 = null,
    };

This is useful when, for instance, interacting with C code compiled with the
`-mpreferred-stack-boundary` GCC flag.

A small number of calling conventions have more complex options, for instance:

    
    
    /// Options for x86 calling conventions which support the regparm attribute to pass some
    /// arguments in registers.
    pub const X86RegparmOptions = struct {
        /// The boundary the stack is aligned to when the function is called.
        /// `null` means the default for this calling convention.
        incoming_stack_alignment: ?u64 = null,
        /// The number of arguments to pass in registers before passing the remaining arguments
        /// according to the calling convention.
        /// Equivalent to `__attribute__((regparm(x)))` in Clang and GCC.
        register_params: u2 = 0,
    };

**The default C calling convention is no longer represented by a special
tag.** Instead, `CallingConvention` contains a declaration named `c` which is
defined as follows:

    
    
    /// This is an alias for the default C calling convention for this target.
    /// Functions marked as `extern` or `export` are given this calling convention by default.
    pub const c = builtin.target.cCallingConvention().?;

When combined with Decl Literals, this permits writing `callconv(.c)` to
specify this calling convention.

Zig 0.14.0 includes declarations named `Unspecified`, `C`, `Naked`, `Stdcall`,
etc, to allow existing usages of `callconv` to continue working thanks to Decl
Literals. These declarations are deprecated, and will be removed in a future
version of Zig.

As previously mentioned, most calling conventions have an
`incoming_stack_alignment` options to specify the byte boundary the stack will
be aligned to when a function is called, which can be used to interop with
code using stack alignments lower than the ABI mandates. Previously, the
`@setAlignStack` builtin could be used for this use case; however, its
behavior was somewhat ill-defined, and applying it to this use case required
knowing the expected stack alignment for your ABI. As such, the
`@setAlignStack` builtin has been removed. Instead, users should annotate on
their `callconv` the expected stack alignment, allowing the optimizer to
realign if necessary. This also allows the optimizer to _avoid_ unnecessarily
realigning the stack when such a function is called. For convenience,
`CallingConvention` has a `withStackAlign` function which can be used to
change the incoming stack alignment. Upgrading is generally fairly simple:

    
    
    // This function will be called by C code which uses a 4-byte aligned stack.
    export fn foo() void {
        // I know that my target's ABI expects a 16-byte aligned stack.
        @setAlignStack(16);
        // ...
    }

⬇️

    
    
    // This function will be called by C code which uses a 4-byte aligned stack.
    // We simply specify that on the `callconv`.
    export fn foo() callconv(.withStackAlign(.c, 4)) void {
        // ...
    }

### std.builtin.Type Fields Renamed §

In most cases, Zig's standard library follows [naming
conventions](https://ziglang.org/documentation/0.14.0/#Names). Zig 0.14.0
updates the fields of the `std.builtin.Type` tagged union to follow these
conventions by lowercasing them:

    
    
    pub const Type = union(enum) {
        type: void,
        void: void,
        bool: void,
        noreturn: void,
        int: Int,
        float: Float,
        pointer: Pointer,
        array: Array,
        @"struct": Struct,
        comptime_float: void,
        comptime_int: void,
        undefined: void,
        null: void,
        optional: Optional,
        error_union: ErrorUnion,
        error_set: ErrorSet,
        @"enum": Enum,
        @"union": Union,
        @"fn": Fn,
        @"opaque": Opaque,
        frame: Frame,
        @"anyframe": AnyFrame,
        vector: Vector,
        enum_literal: void,
        // ...
    };

Note that this requires using "quoted identifier" syntax for `@"struct"`,
`@"union"`, `@"enum"`, `@"opaque"`, and `@"anyframe"`, because these
identifiers are also keywords.

This change is widely breaking, but upgrading is simple:

    
    
    test "switch on type info" {
        const x = switch (@typeInfo(u8)) {
            .Int => 0,
            .ComptimeInt => 1,
            .Struct => 2,
            else => 3,
        };
        try std.testing.expect(0, x);
    }
    test "reify type" {
        const U8 = @Type(.{ .Int = .{
            .signedness = .unsigned,
            .bits = 8,
        } });
        const S = @Type(.{ .Struct = .{
            .layout = .auto,
            .fields = &.{},
            .decls = &.{},
            .is_tuple = false,
        } });
        try std.testing.expect(U8 == u8);
        try std.testing.expect(@typeInfo(S) == .Struct);
    }
    const std = @import("std");

⬇️

    
    
    test "switch on type info" {
        const x = switch (@typeInfo(u8)) {
            .int => 0,
            .comptime_int => 1,
            .@"struct" => 2,
            else => 3,
        };
        try std.testing.expect(0, x);
    }
    test "reify type" {
        const U8 = @Type(.{ .int = .{
            .signedness = .unsigned,
            .bits = 8,
        } });
        const S = @Type(.{ .@"struct" = .{
            .layout = .auto,
            .fields = &.{},
            .decls = &.{},
            .is_tuple = false,
        } });
        try std.testing.expect(U8 == u8);
        try std.testing.expect(@typeInfo(S) == .@"struct");
    }
    const std = @import("std");

### std.builtin.Type.Pointer.Size Field Renamed §

The fields of the `std.builtin.Type.Pointer.Size` enum have been renamed to
lowercase, just like the fields of `std.builtin.Type`. Again, this is a
breaking change, but one which is very easily updated to:

    
    
    test "pointer type info" {
        comptime assert(@typeInfo(*u8).pointer.size == .One);
    }
    test "reify pointer" {
        comptime assert(@Type(.{ .pointer = .{
            .size = .One,
            .is_const = false,
            .is_volatile = false,
            .alignment = 0,
            .address_space = .generic,
            .child = u8,
            .is_allowzero = false,
            .sentinel_ptr = null,
        } }) == *u8);
    }
    const assert = @import("std").debug.assert;

⬇️

    
    
    test "pointer type info" {
        comptime assert(@typeInfo(*u8).pointer.size == .one);
    }
    test "reify pointer" {
        comptime assert(@Type(.{ .pointer = .{
            .size = .one,
            .is_const = false,
            .is_volatile = false,
            .alignment = 0,
            .address_space = .generic,
            .child = u8,
            .is_allowzero = false,
            .sentinel_ptr = null,
        } }) == *u8);
    }
    const assert = @import("std").debug.assert;

### Simplify Usage Of ?*const anyopaque In std.builtin.Type §

The `default_value` field on `std.builtin.Type.StructField`, and the
`sentinel` fields on `std.builtin.Type.Array` and `std.builtin.Type.Pointer`,
have to use `?*const anyopaque`, because Zig does not provide a way for the
struct's type to depend on a field's value. This isn't a problem; however, it
isn't particularly ergonomic at times.

Zig 0.14.0 renames these fields to `default_value_ptr` and `sentinel_ptr`
respectively, and adds helper methods `defaultValue()` and `sentinel()` to
load the value with the correct type as an optional.

    
    
    test "get pointer sentinel" {
        const T = [:0]const u8;
        const ptr = @typeInfo(T).pointer;
        const s = @as(*const ptr.child, @ptrCast(@alignCast(ptr.sentinel.?))).*;
        comptime assert(s == 0);
    }
    test "reify array" {
        comptime assert(@Type(.{ .array = .{ .len = 1, .child = u8, .sentinel = null } }) == [1]u8);
        comptime assert(@Type(.{ .array = .{ .len = 1, .child = u8, .sentinel = &@as(u8, 0) } }) == [1:0]u8);
    }
    const assert = @import("std").debug.assert;

⬇️

    
    
    test "get pointer sentinel" {
        const T = [:0]const u8;
        const ptr = @typeInfo(T).pointer;
        const s = ptr.sentinel().?;
        comptime assert(s == 0);
    }
    test "reify array" {
        comptime assert(@Type(.{ .array = .{ .len = 1, .child = u8, .sentinel_ptr = null } }) == [1]u8);
        comptime assert(@Type(.{ .array = .{ .len = 1, .child = u8, .sentinel_ptr = &@as(u8, 0) } }) == [1:0]u8);
    }
    const assert = @import("std").debug.assert;

### Non-Scalar Sentinel Types Disallowed §

Sentinel values are now forbidden from being aggregate types. In other words,
only types that support the `==` operator are allowed.

non_scalar_sentinel.zig

    
    
    export fn foo() void {
        const S = struct { a: u32 };
        var arr = [_]S{ .{ .a = 1 }, .{ .a = 2 } };
        const s = arr[0..1 :.{ .a = 1 }];
        _ = s;
    }

Shell

    
    
    $ zig test non_scalar_sentinel.zig
    src/download/0.14.0/release-notes/non_scalar_sentinel.zig:4:26: error: non-scalar sentinel type 'non_scalar_sentinel.foo.S'
        const s = arr[0..1 :.{ .a = 1 }];
                            ~^~~~~~~~~~
    src/download/0.14.0/release-notes/non_scalar_sentinel.zig:2:15: note: struct declared here
        const S = struct { a: u32 };
                  ^~~~~~~~~~~~~~~~~
    referenced by:
        foo: src/download/0.14.0/release-notes/non_scalar_sentinel.zig:1:1
    
    

### @FieldType builtin §

Zig 0.14.0 introduces the `@FieldType` builtin. This serves the same purpose
as the `std.meta.FieldType` function: given a type and the name of one of its
fields, it returns the type of that field.

fieldtype.zig

    
    
    const assert = @import("std").debug.assert;
    test "struct @FieldType" {
        const S = struct { a: u32, b: f64 };
        comptime assert(@FieldType(S, "a") == u32);
        comptime assert(@FieldType(S, "b") == f64);
    }
    test "union @FieldType" {
        const U = union { a: u32, b: f64 };
        comptime assert(@FieldType(U, "a") == u32);
        comptime assert(@FieldType(U, "b") == f64);
    }
    test "tagged union @FieldType" {
        const U = union(enum) { a: u32, b: f64 };
        comptime assert(@FieldType(U, "a") == u32);
        comptime assert(@FieldType(U, "b") == f64);
    }

Shell

    
    
    $ zig test fieldtype.zig
    1/3 fieldtype.test.struct @FieldType...OK
    2/3 fieldtype.test.union @FieldType...OK
    3/3 fieldtype.test.tagged union @FieldType...OK
    All 3 tests passed.
    

### @src Gains Module Field §

`std.builtin.SourceLocation`:

    
    
    pub const SourceLocation = struct {
        /// The name chosen when compiling. Not a file path.
        module: [:0]const u8,
        /// Relative to the root directory of its module.
        file: [:0]const u8,
        fn_name: [:0]const u8,
        line: u32,
        column: u32,
    };

The `module` field is new.

### @memcpy Rules Adjusted §

  * The langspec definition of `@memcpy` has been changed so that the source and destination element types must be in-memory coercible, allowing all such calls to be raw copying operations, not actually applying any coercions.
  * Implement aliasing check for comptime `@memcpy`; a compile error will now be emitted if the arguments alias.
  * Implement more efficient comptime `@memcpy` by loading and storing a whole array at once, similar to how `@memset` is implemented.

This is a breaking change because while the old coercion behavior triggered an
"unimplemented" compile error at runtime, it did actually work at comptime.

### Unsafe In-Memory Coercions Disallowed §

[#22243](https://github.com/ziglang/zig/pull/22243)

### callconv, align, addrspace, linksection Cannot Reference Function
Arguments §

[#22264](https://github.com/ziglang/zig/pull/22264)

### Branch Quota Rules Adjusted for Function Calls §

[#22414](https://github.com/ziglang/zig/pull/22414)

## Standard Library §

Uncategorized changes:

  * mem: handle Float and Bool cases in byteSwapAllFields
  * fmt: remove placeholders from binary

### DebugAllocator §

`GeneralPurposeAllocator` relied on a compile-time known page size, so it had
to be rewritten. It is now rewritten to make fewer active mappings, to have
better performance, and is renamed to `DebugAllocator`.

Performance data point. This is running ast-check with a debug zig compiler,
before/after the rewrite.

    
    
    Benchmark 1 (3 runs): master/bin/zig ast-check ../lib/compiler_rt/udivmodti4_test.zig
      measurement          mean ± σ            min … max           outliers         delta
      wall_time          22.8s  ±  184ms    22.6s  … 22.9s           0 ( 0%)        0%
      peak_rss           58.6MB ± 77.5KB    58.5MB … 58.6MB          0 ( 0%)        0%
      cpu_cycles         38.1G  ± 84.7M     38.0G  … 38.2G           0 ( 0%)        0%
      instructions       27.7G  ± 16.6K     27.7G  … 27.7G           0 ( 0%)        0%
      cache_references   1.08G  ± 4.40M     1.07G  … 1.08G           0 ( 0%)        0%
      cache_misses       7.54M  ± 1.39M     6.51M  … 9.12M           0 ( 0%)        0%
      branch_misses       165M  ±  454K      165M  …  166M           0 ( 0%)        0%
    Benchmark 2 (3 runs): branch/bin/zig ast-check ../lib/compiler_rt/udivmodti4_test.zig
      measurement          mean ± σ            min … max           outliers         delta
      wall_time          20.5s  ± 95.8ms    20.4s  … 20.6s           0 ( 0%)        ⚡- 10.1% ±  1.5%
      peak_rss           54.9MB ±  303KB    54.6MB … 55.1MB          0 ( 0%)        ⚡-  6.2% ±  0.9%
      cpu_cycles         34.8G  ± 85.2M     34.7G  … 34.9G           0 ( 0%)        ⚡-  8.6% ±  0.5%
      instructions       25.2G  ± 2.21M     25.2G  … 25.2G           0 ( 0%)        ⚡-  8.8% ±  0.0%
      cache_references   1.02G  ±  195M      902M  … 1.24G           0 ( 0%)          -  5.8% ± 29.0%
      cache_misses       4.57M  ±  934K     3.93M  … 5.64M           0 ( 0%)        ⚡- 39.4% ± 35.6%
      branch_misses       142M  ±  183K      142M  …  142M           0 ( 0%)        ⚡- 14.1% ±  0.5%

### SmpAllocator §

An allocator that is designed for ReleaseFast optimization mode, with multi-
threading enabled.

This allocator is a singleton; it uses global state and only one should be
instantiated for the entire process.

This is a "sweet spot" - the implementation is about 200 lines of code and yet
competitive with glibc performance. For example, here is a comparison of Zig
building itself, using glibc malloc vs SmpAllocator:

    
    
    Benchmark 1 (3 runs): glibc/bin/zig build -Dno-lib -p trash
      measurement          mean ± σ            min … max           outliers         delta
      wall_time          12.2s  ± 99.4ms    12.1s  … 12.3s           0 ( 0%)        0%
      peak_rss            975MB ± 21.7MB     951MB …  993MB          0 ( 0%)        0%
      cpu_cycles         88.7G  ± 68.3M     88.7G  … 88.8G           0 ( 0%)        0%
      instructions        188G  ± 1.40M      188G  …  188G           0 ( 0%)        0%
      cache_references   5.88G  ± 33.2M     5.84G  … 5.90G           0 ( 0%)        0%
      cache_misses        383M  ± 2.26M      381M  …  385M           0 ( 0%)        0%
      branch_misses       368M  ± 1.77M      366M  …  369M           0 ( 0%)        0%
    Benchmark 2 (3 runs): SmpAllocator/fast/bin/zig build -Dno-lib -p trash
      measurement          mean ± σ            min … max           outliers         delta
      wall_time          12.2s  ± 49.0ms    12.2s  … 12.3s           0 ( 0%)          +  0.0% ±  1.5%
      peak_rss            953MB ± 3.47MB     950MB …  957MB          0 ( 0%)          -  2.2% ±  3.6%
      cpu_cycles         88.4G  ±  165M     88.2G  … 88.6G           0 ( 0%)          -  0.4% ±  0.3%
      instructions        181G  ± 6.31M      181G  …  181G           0 ( 0%)        ⚡-  3.9% ±  0.0%
      cache_references   5.48G  ± 17.5M     5.46G  … 5.50G           0 ( 0%)        ⚡-  6.9% ±  1.0%
      cache_misses        386M  ± 1.85M      384M  …  388M           0 ( 0%)          +  0.6% ±  1.2%
      branch_misses       377M  ±  899K      377M  …  378M           0 ( 0%)        💩+  2.6% ±  0.9%

Basic design:

Each thread gets a separate freelist, however, the data must be recoverable
when the thread exits. We do not directly learn when a thread exits, so
occasionally, one thread must attempt to reclaim another thread's resources.

Above a certain size, those allocations are memory mapped directly, with no
storage of allocation metadata. This works because the implementation refuses
resizes that would move an allocation from small category to large category or
vice versa.

Each allocator operation checks the thread identifier from a threadlocal
variable to find out which metadata in the global state to access, and
attempts to grab its lock. This will usually succeed without contention,
unless another thread has been assigned the same id. In the case of such
contention, the thread moves on to the next thread metadata slot and repeats
the process of attempting to obtain the lock.

By limiting the thread-local metadata array to the same number as the CPU
count, ensures that as threads are created and destroyed, they cycle through
the full set of freelists.

To use it, put something like this in your main function:

    
    
    var debug_allocator: std.heap.DebugAllocator(.{}) = .init;
    
    pub fn main() !void {
        const gpa, const is_debug = gpa: {
            if (native_os == .wasi) break :gpa .{ std.heap.wasm_allocator, false };
            break :gpa switch (builtin.mode) {
                .Debug, .ReleaseSafe => .{ debug_allocator.allocator(), true },
                .ReleaseFast, .ReleaseSmall => .{ std.heap.smp_allocator, false },
            };
        };
        defer if (is_debug) {
            _ = debug_allocator.deinit();
        };
    }

[devlog entry](https://ziglang.org/devlog/2025/#2025-02-07)

### Allocator API Changes (remap) §

This release introduces a new function to `std.mem.Allocator.VTable` called
`remap`. The key part from the doc comments:

> Attempt to expand or shrink memory, allowing relocation.
>
> A non-`null` return value indicates the resize was successful. The
> allocation may have same address, or may have been relocated. In either
> case, the allocation now has size of `new_len`. A `null` return value
> indicates that the resize would be equivalent to allocating new memory,
> copying the bytes from the old memory, and then freeing the old memory. In
> such case, it is more efficient for the caller to perform the copy.
    
    
    remap: *const fn (*anyopaque, memory: []u8, alignment: Alignment, new_len: usize, return_address: usize) ?[*]u8,

`resize` remains unchanged with the same semantics.

All the `Allocator.VTable` functions now take a `std.mem.Alignment` type
rather than `u8`. The numerical value is the same, but now there is type
safety and handy methods attached to the type.

Both `resize` and `remap` have their places. For example, `resize` is
necessary for `std.heap.ArenaAllocator` which must not relocate its
allocations. Meanwhile, `remap` is appropriate for `std.ArrayList` when the
capacity increases.

It's important to remember with `remap` that an `Allocator` implementation
should generally behave the same as `resize`, _unless_ the remap can be done
without performing the memcpy inside the allocator.

For instance, this release introduces support for calling `mremap` when
supported, in which case the operating system remaps the pages, avoiding an
expensive memcpy in userspace. Zig programmers can now expect this to happen
when using `std.heap.page_allocator` as well as when using it as a backing
allocator for e.g. `std.heap.ArenaAllocator` or
`std.heap.GeneralPurposeAllocator`.

Additionally:

  * `std.heap.page_allocator` now supports alignments greater than page size, which was needed for the DebugAllocator rewrite.
  * delete `std.heap.WasmPageAllocator` in favor of `std.heap.WasmAllocator`
  * delete `std.heap.LoggingAllocator` did not belong in std, at least not in its current form
  * delete `std.heap.HeapAllocator` \- this was Windows-only and depended on kernel32

### ZON Parsing and Serialization §

`std.zon.parse` provides functionality for parsing ZON into a Zig struct at
runtime:

  * `std.zon.parse.fromSlice`
  * `std.zon.parse.fromZoir`
  * `std.zon.parse.fromZoirNode`
  * `std.zon.parse.free`

Typical use cases will use `std.zon.parse.fromSlice`, and `std.zon.parse.free`
if the type requires allocation.

For ZON values with schemas that don't map cleanly to Zig structs,
`std.zig.ZonGen` can be used to generate a tree structure (`std.Zoir`) that
can be interpreted as desired. For importing ZON at compile time, see Import
ZON.

`std.zon.stringify` provides functionality for serializing ZON at runtime:

  * `std.zon.stringify.serialize`
  * `std.zon.stringify.serializeMaxDepth`
  * `std.zon.stringify.serializeArbitraryDepth`
  * `std.zon.stringify.serializer`

Typical use cases will use `serialize`, or one of its variants.

`std.zon.stringify.serializer` returns a more fine grained interface. It may
be used to serialize a value piece by piece, for example to apply different
configuration to different parts of the value or to serialize a value in a
different form than it is laid out in memory.

### Runtime Page Size §

Compile time known `std.mem.page_size` is removed, which is a nonsensical
concept since the page size is in fact runtime-known (sorry about that), and
replaces it with `std.heap.page_size_min` and `std.heap.page_size_max` for
comptime-known bounds of possible page sizes. Uses of `std.mem.page_size` in
pointer alignment properties, such as in mmap, are migrated to
`std.heap.page_size_min`.

In places where the page size must be used, `std.heap.pageSize()` provides the
answer. It will return a comptime-known value if possible, otherwise querying
the operating system at runtime, and memoizing the result (atomically, of
course). It also has a `std.options` integration so the application maintainer
has the ability to override this behavior.

Notably, this fixes support for Linux running on Apple's new hardware, such as
[Asahi Linux](https://asahilinux.org/).

### Panic Interface §

[22594](https://github.com/ziglang/zig/pull/22594)

### Transport Layer Security (std.crypto.tls) §

[#21872](https://github.com/ziglang/zig/pull/21872)

### process.Child.collectOutput API Changed §

Upgrade guide:

    
    
    var stdout = std.ArrayList(u8).init(allocator);
    defer stdout.deinit();
    var stderr = std.ArrayList(u8).init(allocator);
    defer stderr.deinit();
    
    try child.collectOutput(&stdout, &stderr, max_output_bytes);

↓

    
    
    var stdout: std.ArrayListUnmanaged(u8) = .empty;
    defer stdout.deinit(allocator);
    var stderr: std.ArrayListUnmanaged(u8) = .empty;
    defer stderr.deinit(allocator);
    
    try child.collectOutput(allocator, &stdout, &stderr, max_output_bytes);

Before, `collectOutput` included a check to ensure that `stdout.allocator` was
the same as `stderr.allocator`, which was necessary due to its internal
implementation. However, comparing the `ptr` field of an `Allocator` interface
can lead to illegal behavior, since `Allocator.ptr` is set to undefined in
cases where the allocator implementation does not have any associated state
(`page_allocator`, `c_allocator`, etc).

With this change, that unsafe `Allocator.ptr` comparison has been eliminated
from `collectOutput` (and it was the only occurrence of such a comparison in
the Zig codebase). Additionally, the documentation for the `ptr` field of both
the `Allocator` and `Random` interfaces has been updated to mention that any
comparison of those fields could lead to illegal behavior. In the future, this
comparison [will become detectable illegal
behavior](https://github.com/ziglang/zig/issues/211).

### LLVM Builder API §

Zig is one of very few compilers that emit LLVM bitcode directly, rather than
relying on libLLVM which has an unstable API and is very large. This is part
of our efforts toward entirely eliminating the LLVM dependency from Zig
([#16270](https://github.com/ziglang/zig/issues/16270)). The Roc project
recently
[decided](https://gist.github.com/rtfeldman/77fb430ee57b42f5f2ca973a3992532f)
to rewrite their compiler in Zig, partly motivated by being able to reuse
Zig's LLVM bitcode builder. To make this even easier, we've decided to move
the builder API to `std.zig.llvm` for third-party projects to use. Do note
that, as with everything else in the `std.zig` namespace, this is an
implementation detail of the Zig compiler and is not necessarily subject to
the same API stability and deprecation norms as the rest of the standard
library.

### Embracing "Unmanaged"-Style Containers §

`std.ArrayHashMap` is now deprecated and aliased to
`std.ArrayHashMapWithAllocator`.

To upgrade, switch to `ArrayHashMapUnmanaged` which will entail updating
callsites to pass an allocator to methods that need one. After Zig 0.14.0 is
released, `std.ArrayHashMapWithAllocator` will be removed and
`std.ArrayHashMapUnmanaged` will be a deprecated alias of `ArrayHashMap`.
After Zig 0.15.0 is released, the deprecated alias `ArrayHashMapUnmanaged`
will be removed.

This move comes from unanimous agreement among veteran Zig users who have
converged on the "unmanaged" container variants. They act as better building
blocks, avoiding storing the same data redundantly, and the presence/absence
of the allocator parameter dovetails nicely with the reserve capacity /
reserved insertion pattern.

The other "managed" container variants are also deprecated, such as
`std.ArrayList`.

    
    
    var list = std.ArrayList(i32).init(gpa);
    defer list.deinit();
    try list.append(1234);
    try list.ensureUnusedCapacity(1);
    list.appendAssumeCapacity(5678);

⬇️

    
    
    const ArrayList = std.ArrayListUnmanaged;
    var list: std.ArrayList(i32) = .empty;
    defer list.deinit(gpa);
    try list.append(gpa, 1234);
    try list.ensureUnusedCapacity(gpa, 1);
    list.appendAssumeCapacity(5678);

### List of Deprecations §

Deprecated aliases that are now compile errors:

  * `std.fs.MAX_PATH_BYTES` (renamed to `std.fs.max_path_bytes`)
  * `std.mem.tokenize` (split into `tokenizeAny`, `tokenizeSequence`, `tokenizeScalar`)
  * `std.mem.split` (split into `splitSequence`, `splitAny`, `splitScalar`)
  * `std.mem.splitBackwards` (split into `splitBackwardsSequence`, `splitBackwardsAny`, `splitBackwardsScalar`)
  * `std.unicode`
    * `utf16leToUtf8Alloc`, `utf16leToUtf8AllocZ`, `utf16leToUtf8`, `fmtUtf16le` (all renamed to have capitalized `Le`)
    * `utf8ToUtf16LeWithNull` (renamed to `utf8ToUtf16LeAllocZ`)
  * `std.zig.CrossTarget` (moved to `std.Target.Query`)
  * std.fs.Dir: Rename OpenDirOptions to OpenOptions
  * `std.crypto.tls.max_cipertext_inner_record_len` renamed to `std.crypto.tls.max_ciphertext_inner_record_len`

Deprecated `lib/std/std.zig` decls were deleted instead of made a
`@compileError` because the `refAllDecls` in the test block would trigger the
`@compileError`. The deleted top-level `std` namespaces are:

  * `std.rand` (renamed to `std.Random`)
  * `std.TailQueue` (renamed to `std.DoublyLinkedList`)
  * `std.ChildProcess` (renamed/moved to `std.process.Child`)

More deprecations:

  * std.posix.iovec: use .base and .len instead of .iov_base and .iov_len
  * `LockViolation` was added to `std.posix.ReadError`. This error will occur if `std.os.windows.ReadFile` encounters `ERROR_LOCK_VIOLATION`.
  * `popOrNull` renamed to `pop` in all container types.

### std.c Reorganization §

It is now composed of these main sections:

  * Declarations that are shared among all operating systems.
  * Declarations that have the same name, but different type signatures depending on the operating system. Often multiple operating systems share the same type signatures however.
  * Declarations that are specific to a single operating system.
    * These are imported one per line so you can see where they come from, protected by a comptime block inside the OS-specific file to prevent accessing the wrong one.
  * A namespace called `private` at the bottom that is a bag of decls for logic above to pick and choose from.

Closes [#19352](https://github.com/ziglang/zig/issues/19352) by changing the
convention for nonexisting symbols from `@compileError` to making types `void`
and functions `{}`, so that it becomes possible to update `@hasDecl` sites to
use `@TypeOf(f) != void` or `T != void`. Happily, this ended up removing some
duplicate logic and update some bitrotted feature detection checks.

A handful of types have been modified to gain namespacing, type safety, and
conform to field naming conventions. This is a breaking change.

With this, the last usage of `usingnamespace` site is eliminated from the
standard library.

### Binary Search §

[#20927](https://github.com/ziglang/zig/pull/20927)

### std.hash_map gains a rehash method §

Unordered hash maps currently have a nasty flaw: [removals cause HashMaps to
become slow](https://github.com/ziglang/zig/issues/17851).

In the future, hash maps will be adjusted to not have this flaw, and this
method will be unceremoniously deleted.

Note that array hash maps do _not_ have this flaw.

## Build System §

Uncategorized changes:

  * Report error on missing values for addConfigHeader
  * fix WriteFile and addCSourceFiles not adding LazyPath deps
  * **[Breaking]** `Compile.installHeader` now takes a `LazyPath`.
  * **[Breaking]** `Compile.installConfigHeader` has had its second argument removed and now uses the value of `include_path` as its sub path, for parity with `Module.addConfigHeader`. Use `artifact.installHeader(config_h.getOutput(), "foo.h")` if you want to set the sub path to something different.
  * **[Breaking]** `Compile.installHeadersDirectory/installHeadersDirectoryOptions` have been consolidated into `Compile.installHeadersDirectory`, which takes a `LazyPath` and allows exclude/include filters just like `InstallDir`.
  * **[Breaking]** `b.addInstallHeaderFile` now takes a `LazyPath`.
  * **[Breaking]** As a workaround for [#9698](https://github.com/ziglang/zig/issues/9698), the generated `-femit-h` header is now never emitted even when the user specifies an override for `h_dir`. If you absolutely need the emitted header, you now need to do `install_artifact.emitted_h = artifact.getEmittedH()` until `-femit-h` is fixed.
  * added `WriteFile.addCopyDirectory`, which functions very similar to `InstallDir`.
  * `InstallArtifact` has been updated to install the bundled headers alongide the artifact. The bundled headers are installed to the directory specified by `h_dir` (which is `zig-out/include` by default).
  * std.Build: Detect pkg-config names with "lib" prefix
  * fetch: add support for SHA-256 Git repositories
  * fetch: add executable detection for Mach-O file headers
  * Allow ConfigHeader values to be added outside of comptime

### File System Watching §

    
    
      --watch                      Continuously rebuild when source files are modified
      --debounce <ms>              Delay before rebuilding after changed file detected
    

Uses the build system's perfect knowledge of all file system inputs to the
pipeline to keep the build runner alive after completion, watching the minimal
number of directories in order to trigger re-running only the dirty steps from
the graph.

Default debounce time is 50ms but this is configurable. It helps prevent
wasted rebuilds when source files are changed in rapid succession, for example
when saving with vim it does not do an atomic rename into place but actually
deletes the destination file before writing it again, causing a brief period
of invalid state, which would cause a build failure without debouncing (it
would be followed by a successful build, but it's annoying to experience the
temporary build failure regardless).

The purpose of this feature is to reduce latency between editing and debugging
in the development cycle. In large projects, the cache system must call
`fstat` on a large number of files even when it is a cache hit. File system
watching allows more efficient detection of stale pipeline steps.

Mainly this is motivated by Incremental Compilation landing soon, so that we
can keep the compiler running and responding to source code changes as fast as
possible. In this case, also keeping the rest of the build pipeline up-to-date
is table stakes.

### New Package Hash Format §

Old hashes look like this:
`1220115ff095a3c970cc90fce115294ba67d6fbc4927472dc856abc51e2a1a9364d7`

New hashes look like this: `mime-3.0.0-zwmL-6wgAADuFwn7gr-
_DAQDGJdIim94aDIPa6qO-6GT`

Along with 200 bits of SHA-256, new hashes have the following additional data
inside them:

  * name
  * version
  * id component of the fingerprint
  * total unpacked size on disk

This provides a better user experience when package hashes show up in compile
errors or file paths, and provides the data needed for implementing dependency
tree management tooling. For instance, by knowing only the package hashes of
the entire dependency tree, it is now possible to know the total file size on
disk that will be required after all fetching is complete, as well as
performing version selection, _without doing any fetching_.

The file size can also be used as a heuristic when deciding whether to fetch
lazy packages by default.

These benefits require some new rules that govern `build.zig.zon` files:

  * `name` and `version` are limited to 32 bytes.
  * `name` must be a valid bare Zig-identifier. In the future, this restriction may be lifted; a conservative rule was chosen for now.

`fingerprint` is an important concept to understand:

Together with `name`, this represents a globally unique package identifier.
This field is auto-initialized by the toolchain when the package is first
created, and then _never changes_. Despite the ecosystem being decentralized,
this allows Zig to unambiguously detect when one package is an updated version
of another.

When forking a Zig project, this fingerprint should be regenerated if the
upstream project is still maintained. Otherwise, the fork is _hostile_ ,
attempting to take control over the original project's identity. The
fingerprint can be regenerated by deleting the field and running `zig build`.

This 64-bit integer is the combination of a 32-bit id component and a 32-bit
checksum.

The id component within the fingerprint has these restrictions:

`0x00000000` is reserved for legacy packages.

`0xffffffff` is reserved to represent "naked" packages.

The checksum is computed from `name` and serves to protect Zig users from
accidental id collisions.

Version selection and related tooling that takes advantage of `fingerprint` is
not implemented yet.

Although the legacy hash format is still supported, this change breaks any
packages that do not already happen to follow the new package naming rules
outlined above. There is also a known bug: [legacy packages are unnecessarily
fetched](https://github.com/ziglang/zig/issues/23051).

### WriteFile Step §

If you were using `WriteFile` for its ability to update source files, that
functionality has been extracted into a separate step called
`UpdateSourceFiles`. Everything else is the same, so migration looks like
this:

    
    
    -    const copy_zig_h = b.addWriteFiles();
    +    const copy_zig_h = b.addUpdateSourceFiles();
    

### RemoveDir Step §

If you were using a `RemoveDir` step, it now takes a `LazyPath` instead of
`[]const u8`. Probably your migration looks like this:

    
    
    -        const cleanup = b.addRemoveDirTree(tmp_path);
    +        const cleanup = b.addRemoveDirTree(.{ .cwd_relative = tmp_path });
    

However, please consider not choosing a temporary path at configure time as
this is somewhat brittle when it comes to running your build pipeline
concurrently.

### Fmt Step §

This step now prints file names that failed the format check.

### Creating Artifacts from Existing Modules §

Zig 0.14.0 modifies the build system APIs for creating `Compile` steps,
allowing them to be created from existing `std.Build.Module` objects. This
allows for module graphs to be defined in a more clear manner, and for
components of these graphs to be reused more easily; for instance, a module
which exists as a dependency of another can easily have a corresponding test
step created. The new APIs can be used by modifying your calls to
`addExecutable`, `addTest`, etc. Instead of passing options like
`root_source_file`, `target`, and `optimize` directly to these functions, you
should pass in the `root_module` field a `*std.Build.Module` created using
these parameters. Zig 0.14.0 still permits the old, deprecated usages for
these functions; the next release will remove them.

Users of the legacy APIs can upgrade with minimal effort by just moving the
module-specific parts of their `addExecutable` (etc) call into a
`createModule` call. For instance, here is the updated version of a simple
build script:

    
    
    pub fn build(b: *std.Build) void {
        const target = b.standardTargetOptions(.{});
        const optimize = b.standardOptimizeOption(.{});
    
        const exe = b.addExecutable(.{
            .name = "hello",
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        });
        b.installArtifact(exe);
    }
    const std = @import("std");

⬇️

    
    
    pub fn build(b: *std.Build) void {
        const target = b.standardTargetOptions(.{});
        const optimize = b.standardOptimizeOption(.{});
    
        const exe = b.addExecutable(.{
            .name = "hello",
            .root_module = b.createModule(.{ // this line was added
                .root_source_file = b.path("src/main.zig"),
                .target = target,
                .optimize = optimize,
            }), // this line was added
        });
        b.installArtifact(exe);
    }
    const std = @import("std");

And, to demostrate the benefits of the new API, here is an example build
script which elegantly constructs a complex build graph of multiple modules:

    
    
    pub fn build(b: *std.Build) void {
        const target = b.standardTargetOptions(.{});
        const optimize = b.standardOptimizeOption(.{});
    
        // First, we create our 3 modules.
    
        const foo = b.createModule(.{
            .root_source_file = b.path("src/foo.zig"),
            .target = target,
            .optimize = optimize,
        });
        const bar = b.createModule(.{
            .root_source_file = b.path("src/bar.zig"),
            .target = target,
            .optimize = optimize,
        });
        const qux = b.createModule(.{
            .root_source_file = b.path("src/qux.zig"),
            .target = target,
            .optimize = optimize,
        });
    
        // Next, we set up all of their dependencies.
    
        foo.addImport("bar", bar);
        foo.addImport("qux", qux);
        bar.addImport("qux", qux);
        qux.addImport("bar", bar); // mutual recursion!
    
        // Finally, we will create all of our `Compile` steps.
        // `foo` will be the root of an executable, but all 3 modules also have unit tests we want to run.
    
        const foo_exe = b.addExecutable(.{
            .name = "foo",
            .root_module = foo,
        });
    
        b.installArtifact(foo_exe);
    
        const foo_test = b.addTest(.{
            .name = "foo",
            .root_module = foo,
        });
        const bar_test = b.addTest(.{
            .name = "bar",
            .root_module = bar,
        });
        const qux_test = b.addTest(.{
            .name = "qux",
            .root_module = qux,
        });
    
        const test_step = b.step("test", "Run all unit tests");
        test_step.dependOn(&b.addRunArtifact(foo_test).step);
        test_step.dependOn(&b.addRunArtifact(bar_test).step);
        test_step.dependOn(&b.addRunArtifact(qux_test).step);
    }
    const std = @import("std");

### Allow Packages to Expose Arbitrary LazyPaths by Name §

In previous versions of Zig, packges could expose _artifacts_ , _modules_ ,
and _named`WriteFile` steps_. These can be exposed through `installArtifact`,
`addModule`, and `addNamedWriteFiles` respectively, and can be accessed
through methods on `std.Build.Dependency`. In addition to these, Zig 0.14.0
introduces the ability for packages for expose arbitrary `LazyPath`s. A
dependency exposes them with `std.Build.addNamedLazyPath`, and a dependant
package uses `std.Build.Dependency.namedLazyPath` to access them.

One use case for this function is for a dependency to expose a generated file
to its dependant package. For instance, in the following example, the
dependency package `bar` exposes a generated Zig file which is used by the
main package as a module import of an executable:

build.zig

    
    
    pub fn build(b: *std.Build) void {
        const target = b.standardTargetOptions(.{});
        const optimize = b.standardOptimizeOption(.{});
        const bar = b.dependency("bar", .{});
        const exe = b.addExecutable(.{
            .name = "main",
            .root_source_file = b.path("main.zig"),
            .target = target,
            .optimize = optimize,
        });
        exe.root_module.addImport("generated", bar.namedLazyPath("generated"));
        b.installArtifact(exe);
    }

bar/build.zig

    
    
    pub fn build(b: *std.Build) {
        const generator = b.addExecutable(.{
            .name = "generator",
            .root_source_file = b.path("generator.zig"),
            .target = b.graph.host,
            .optimize = .ReleaseSafe,
        });
        const run_gen = b.addRunArtifact(generator);
        const generated_file = run_gen.addOutputFileArg("generated.zig");
        b.addNamedLazyPath("generated", generated_file);
    }

### addLibrary Function §

Acts as a replacement for `addSharedLibrary` and `addStaticLibrary`, but
linking mode can be changed more easily in build.zig, for example:

In library:

    
    
    const linkage = b.option(std.builtin.LinkMode, "linkage", "Link mode for a foo_bar library") orelse .static; // or other default
        
    const lib = b.addLibrary(.{
        .linkage = linkage,
        .name = "foo_bar",
        .root_module = mod,
    });

In consumer:

    
    
    const dep_foo_bar = b.dependency("foo_bar", .{
        .target = target,
        .optimize = optimize,
        .linkage = .dynamic // or leave for default static
    });
    
    mod.linkLibrary(dep_foor_bar.artifact("foo_bar"));

It also matches nicely with `linkLibrary` name.

## Compiler §

Uncategorized changes:

  * `-fno-omit-frame-pointer` is now the default for ReleaseSmall on x86 targets
  * pipeline: spawn jobs earlier that produce linker inputs

### Multithreaded Backend Support §

Some backends of the compiler, such as x86 Backend, now support running
codegen in a separate thread than the frontend. As a data point, this sped up
the compiler building itself on one computer from 12.8s to 8.57s.

### Incremental Compilation §

Although this feature is not ready to be enabled by default, it can be opted
into via the `-fincremental` flag passed to `zig build`. It is recommended to
be combined with File System Watching, since compiler state serialization is
not implemented yet.

This feature has varying levels of completeness depending on which Linker
backend is being used. None of them are generally ready for use yet, however
it works well combined with `-fno-emit-bin`.

Users are encouraged to create a build option for checking compile errors
only, and try out incremental compilation this way:

    
    
    const no_bin = b.option(bool, "no-bin", "skip emitting binary") orelse false;
    if (no_bin) {
        b.getInstallStep().dependOn(&exe.step);
    } else {
        b.installArtifact(exe);
    }

When working on a large refactor and want quick compile error feedback:

    
    
    $ zig build -Dno-bin -fincremental --watch
    Build Summary: 3/3 steps succeeded
    install success
    └─ zig build-exe zig Debug native success 14s
       └─ options success
    Build Summary: 3/3 steps succeeded
    install success
    └─ zig build-exe zig Debug native success 63ms
    watching 119 directories, 1 processes
        

In the above example, it takes 14s to generate (no) compile errors for a half-
million line codebase. However, because we use `--watch` and `-fincremental`,
after making an edit and saving, it takes only 63ms to perform reanalysis of
only the changed code.

Users who invest in adding a `-Dno-bin` option to their build scripts can
enjoy a similar workflow. In the future, this will be able to generate a fully
working binary as well, which can be tested and debugged like normal.

This feature is not yet compatible with `usingnamespace`. Users are encouraged
to avoid `usingnamespace` as much as possible.

### x86 Backend §

![Zero the Ziguana](https://ziglang.org/img/Zero_2.svg)

The x86 backend is now passing 1884/1923 (98%) of the behavior test suite
compared to the LLVM backend. Although it is not yet selected by default, it
is more often than not a better choice than LLVM backend while developing, due
to dramatically faster compilation speed, combined with [better debugger
support](https://github.com/ziglang/zig/wiki/LLDB-for-Zig).

This backend is nearing completion; it is expected to be selected by default
for debug mode early in the next release cycle. Users are encouraged to try it
out in this 0.14.0 release. It can be selected with `-fno-llvm`, or `use_llvm
= false` in a build script.

### Import ZON §

ZON can now be imported at compile time:

    
    
    const foo: Foo = @import("foo.zon");

For the time being this requires a known result type, there are plans to lift
this restriction in the future. For importing ZON at runtime see ZON Parsing
and Serialization.

### tokenizer: simplification and spec conformance §

I pointed a fuzzer at the tokenizer and it crashed immediately. Upon
inspection, I was dissatisfied with the implementation. This commit removes
several mechanisms:

  * Removes the "invalid byte" compile error note.
  * Dramatically simplifies tokenizer recovery by making recovery always occur at newlines, and never otherwise.
  * Removes UTF-8 validation.
  * Moves some character validation logic to `std.zig.parseCharLiteral`.

Removing UTF-8 validation is a regression of
[#663](https://github.com/ziglang/zig/issues/663), however, the existing
implementation was already buggy. When adding this functionality back, it must
be fuzz-tested while checking the property that it matches an independent
Unicode validation implementation on the same file. While we're at it, fuzzing
should check the other properties of that proposal, such as no ASCII control
characters existing inside the source code, `\r` always followed by `\n`, etc.

Other changes included in this commit:

  * Deprecate `std.unicode.utf8Decode` and its WTF-8 counterpart. This function has an awkward API that is too easy to misuse.
  * Make `utf8Decode2` and friends use arrays as parameters, eliminating a runtime assertion in favor of using the type system.

After this commit, the crash found by fuzzing, which was
`"\x07\xd5\x80\xc3=o\xda|a\xfc{\x9a\xec\x91\xdf\x0f\\\x1a^\xbe;\x8c\xbf\xee\xea"`
no longer causes a crash. However, I did not feel the need to add this test
case because the simplified logic eradicates crashes of this nature.

    
    
    Benchmark 1 (100 runs): before/zig ast-check /home/andy/dev/zig/src/Sema.zig
      measurement          mean ± σ            min … max           outliers         delta
      wall_time          50.0ms ± 2.04ms    48.7ms … 57.4ms         14 (14%)        0%
      peak_rss           60.0MB ±  147KB    59.4MB … 60.2MB          3 ( 3%)        0%
      cpu_cycles          232M  ±  745K      230M  …  234M           3 ( 3%)        0%
      instructions        522M  ± 24.3       522M  …  522M           1 ( 1%)        0%
      cache_references   6.55M  ±  120K     6.39M  … 7.45M           2 ( 2%)        0%
      cache_misses        205K  ± 3.47K      198K  …  215K           1 ( 1%)        0%
      branch_misses      2.86M  ± 10.3K     2.80M  … 2.87M           9 ( 9%)        0%
    Benchmark 2 (104 runs): after/zig ast-check /home/andy/dev/zig/src/Sema.zig
      measurement          mean ± σ            min … max           outliers         delta
      wall_time          48.3ms ±  250us    48.1ms … 50.0ms         10 (10%)        ⚡-  3.3% ±  0.8%
      peak_rss           62.4MB ±  142KB    62.1MB … 62.6MB          0 ( 0%)        💩+  4.1% ±  0.1%
      cpu_cycles          227M  ±  637K      226M  …  230M           7 ( 7%)        ⚡-  1.9% ±  0.1%
      instructions        501M  ± 44.8       501M  …  501M           7 ( 7%)        ⚡-  4.0% ±  0.0%
      cache_references   6.65M  ±  141K     6.45M  … 7.67M           4 ( 4%)          +  1.5% ±  0.5%
      cache_misses        208K  ± 3.79K      201K  …  226K           3 ( 3%)          +  1.3% ±  0.5%
      branch_misses      2.84M  ± 8.62K     2.81M  … 2.86M           1 ( 1%)          -  0.4% ±  0.1%

I also noticed that the tokenizer did not conform to
<https://github.com/ziglang/zig-spec/issues/38> so I fixed it.

### Include Error Trace in All Functions §

[#22572](https://github.com/ziglang/zig/pull/22572)

## Linker §

### Move Input File Parsing to the Frontend §

Moves GNU ld script processing to the frontend to join the relevant library
lookup logic, making the libraries within subject to the same search criteria
as all the other libraries.

This change is necessary so that the compiler has knowledge of all linker
inputs at the start of compilation, so that linking and compilation can begin
at the same time. Finding out about linker inputs during flush() is too late.
This branch fully removes `lib_dirs` from being passed to the ELF linking
code.

This unfortunately means doing file system access on all .so files when
targeting ELF to determine if they are linker scripts, so I introduced an opt-
in CLI flag to enable .so scripts. When a GNU ld script is encountered, the
error message instructs users about the CLI flag that will immediately solve
their problem, which is passing `-fallow-so-scripts` to `zig build`. This
means that users who don't have funky libraries, or at least avoid linking
against them, don't have to pay the cost of these file system accesses.

All object file, archive, and shared object file parsing now happens during
the parallel compilation pipeline rather than bottlenecking at the end.

This is a step towards Incremental Compilation.

### Wasm Linker Rewritten §

The goals of this rewrite were:

  * compile faster when using the wasm linker and backend
  * enable saving compiler state by directly copying in-memory linker state to disk.
  * more efficient compiler memory utilization
  * introduce integer type safety to wasm linker code
  * generate better WebAssembly code
  * fully participate in Incremental Compilation
  * do as much work as possible in the compiler pipeline rather than bottlenecking at the end, while continuing to do garbage collection.
  * avoid unnecessary heap allocations
  * avoid unnecessary indirect function calls

All of these goals were accomplished. Demos and performance data points are
available in [the writeup](https://github.com/ziglang/zig/pull/22220).

Although it is passing the same test suite from before, the linker is not
finished yet, not enabled by default yet, and therefore does not eliminate the
dependency on LLD.

## Fuzzer §

Zig 0.14.0 ships with an integrated fuzzer. It is alpha quality status, which
means that using it requires participating in the development process.

Adds a `--fuzz` CLI option to the build runner. When this is used it rebuilds
any unit test binaries which contained at least one fuzz test with `-ffuzz`
and then tells it to start fuzzing, which does in-process fuzzing.

This contains only a rudimentary implementation of fuzzer logic, really just
some early, early experiments, but already it makes this test case fail in 65
milliseconds on my machine:

    
    
    fn findSecret(context: []const u8, input: []const u8) !void {
        if (std.mem.eql(u8, context, input))
            return error.FoundSecretString;
    }
    test "fuzz example" {
        try std.testing.fuzz(@as([]const u8, "canyoufindme"), findSecret, .{});
    }
    const std = @import("std");

The `--fuzz` flag causes the build system to spawn an HTTP server that
provides a fuzzer web UI, which shows live-updating code coverage as the
fuzzer explores different inputs.

    
    
    $ zig build test --fuzz
    info: web interface listening at http://127.0.0.1:38239/
    info: hint: pass --port 38239 to use this same port next time
    [0/1] Fuzzing
    └─ foo.bar.example

[asciinema demo](https://asciinema.org/a/asgN7rIr6LFeMhQMOXI825wGe)

[video demo and screenshots](https://github.com/ziglang/zig/pull/20958)

## Bug Fixes §

[Full list of the 416 bug reports closed during this release
cycle](https://github.com/ziglang/zig/issues?q=is%3Aclosed+is%3Aissue+label%3Abug+milestone%3A0.14.0).

Many bugs were both introduced and resolved within this release cycle. Most
bug fixes are omitted from these release notes for the sake of brevity.

### This Release Contains Bugs §

![Zero the Ziguana](https://ziglang.org/img/Zero_8.svg)

Zig has [known
bugs](https://github.com/ziglang/zig/issues?q=is%3Aopen+is%3Aissue+label%3Abug),
[miscompilations](https://github.com/ziglang/zig/issues?q=is%3Aopen+is%3Aissue+label%3Amiscompilation),
and
[regressions](https://github.com/ziglang/zig/issues?q=is%3Aopen+is%3Aissue+label%3Aregression).

Even with Zig 0.14.0, working on a non-trivial project using Zig may require
participating in the development process.

When Zig reaches 1.0.0, Tier 1 support will gain a bug policy as an additional
requirement.

## Toolchain §

### UBSan Runtime §

Zig now provides a runtime library for
[UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html), which is
enabled by default when compiling in `Debug` mode.

In summary, by default, when Undefined Behavior is triggered in C code, it
looks like this now:

    
    
    $ zig run test.c -lc
    thread 208135 panic: signed integer overflow: 2147483647 + 2147483647 cannot be represented in type 'int'
    /home/david/Code/zig/build/test.c:4:14: 0x1013e41 in foo (test.c)
        return x + y;
                 ^
    /home/david/Code/zig/build/test.c:8:18: 0x1013e63 in main (test.c)
        int result = foo(0x7fffffff, 0x7fffffff);
                     ^
    ../sysdeps/nptl/libc_start_call_main.h:58:16: 0x7fca4c42e1c9 in __libc_start_call_main (../sysdeps/x86/libc-start.c)
    ../csu/libc-start.c:360:3: 0x7fca4c42e28a in __libc_start_main_impl (../sysdeps/x86/libc-start.c)
    ???:?:?: 0x1013de4 in ??? (???)
    ???:?:?: 0x0 in ??? (???)
    fish: Job 1, 'zig run test.c -lc' terminated by signal SIGABRT (Abort)

If the default does not correctly detect whether the runtime library should be
omitted or included, it can be overridden with `-fno-ubsan-rt` and `-fubsan-
rt`, respectively. [Tracking issue for enhanced default
detection](https://github.com/ziglang/zig/issues/23052).

[devlog entry](/devlog/2025/#2025-02-24)

### compiler_rt §

#### Optimized memcpy §

[#18912](https://github.com/ziglang/zig/pull/18912)

### LLVM 19 §

This release of Zig upgrades to [LLVM
19.1.7](https://releases.llvm.org/19.1.0/docs/ReleaseNotes.html). This covers
Clang (`zig cc`/`zig c++`), libc++, libc++abi, libunwind, and libtsan well.

### musl 1.2.5 §

Zig ships with the source code to [musl](http://musl.libc.org/). When the musl
C ABI is selected, Zig builds static musl from source for the selected target.
Zig also supports targeting dynamically linked musl which is useful for Linux
distributions that use it as their system libc, such as [Alpine
Linux](https://www.alpinelinux.org/).

This release keeps v1.2.5, however:

  * Applies Rich Felker's [CVE-2025-26519 mitigation patches](https://www.openwall.com/lists/oss-security/2025/02/13/2).
  * Applies a number of target-specific patches that are in the process of being upstreamed.
  * Updates the list of libc stub symbols made available when linking dynamically.
  * Fixes a stack overflow in some special libc functions such as `fma` on soft float targets.

Additionally, Zig [no longer ships musl's memcpy
files](https://github.com/ziglang/zig/pull/22513). Instead, Zig provides
Optimized memcpy.

### glibc 2.41 §

glibc versions 2.40 and 2.41 are now available when cross-compiling.

Some notable fixes:

  * Fixed Zig-built executables not defining `_IO_stdin_used`, rendering them unusable on several targets. 
  * Fixed an edge case leading to duplicate stub symbols for certain targets, e.g. `lgammal` on powerpc and s390x. 
  * Changed stub symbols to not all have the same address. This caused LLVM to merge them on some targets, resulting in very broken code. 
  * Applied a workaround for an LLVM bug causing `j $ra` to be assembled incorrectly when targeting mips r6. 
  * Applied a workaround for missing syntax support in LLVM's s390x assembler. 

### Linux 6.13.4 Headers §

This release includes Linux kernel headers for version 6.13.4.

### Darwin libSystem 15.1 §

This release includes Darwin libSystem symbols for Xcode SDK version 15.1.

### MinGW-w64 §

This release bumps the bundled MinGW-w64 copy to commit
`3839e21b08807479a31d5a9764666f82ae2f0356`.

Additional changes:

  * Zig now bundles the winpthreads library.
  * Zig now supports cross-compiling for `thumb-windows-gnu`.

### wasi-libc §

This release bumps the bundled wasi-libc copy to commit
`d03829489904d38c624f6de9983190f1e5e7c9c5`.

## Roadmap §

![Ziggy the Ziguana](https://ziglang.org/img/Ziggy_8.svg)

The major theme of the 0.15.0 release cycle will be **compilation speed**.

Some upcoming milestones we will be working towards:

  * Making the x86 Backend the default backend for debug mode.
  * Enhance Linker implementations, eliminating dependency on [LLD](https://lld.llvm.org/) and supporting Incremental Compilation.
  * Enhance the integrated Fuzzer to be competitive with AFL and other state-of-the-art fuzzers.

The idea here is that prioritizing faster compilation will increase
development velocity on the Compiler itself, leading to more bugs fixed and
features completed in the following release cycles.

It also could potentially lead to Language Changes that unblock fast
compilation.

## Thank You Contributors! §

![Ziggy the Ziguana](https://ziglang.org/img/Ziggy_7.svg)

Here are all the people who landed at least one contribution into this
release:

  * Alex Rønne Petersen
  * Andrew Kelley
  * Matthew Lugg
  * Jakub Konka
  * Jacob Young
  * David Rubin
  * Robin Voetter
  * Linus Groh
  * Frank Denis
  * Ryan Liptak
  * Evan Haas
  * Pavel Verigo
  * Krzysztof Wolicki
  * Meghan Denny
  * Ali Cheraghi
  * Casey Banner
  * YANG Xudong
  * Michael Dusan
  * Techatrix
  * Ian Johnson
  * John Benediktsson
  * Will Lillis
  * 87flowers
  * Dominic
  * Eric Joldasov
  * Pat Tullmann
  * Patrick Wickenhaeuser
  * Tau
  * Wooster
  * Igor Anić
  * Loris Cro
  * Alex Kladov
  * Hugo Beauzée-Luyssen
  * Isaac Freund
  * Jonathan Marler
  * Jarrod Meyer
  * Marc Tiehuis
  * Veikka Tuominen
  * antlilja
  * xdBronch
  * Carter Snook
  * Daniel Hooper
  * Fri3dNstuff
  * Jens Goldberg
  * Lucas Santos
  * Michael Bradshaw
  * Shun Sakai
  * Tw
  * Xavier Bouchoux
  * achan1989
  * clickingbuttons
  * mochalins
  * Carl Åstholm
  * Chris Boesch
  * Constantin Bilz
  * Jan200101
  * Jari Vetoniemi
  * Jay Petacat
  * Jeremy Hertel
  * Josh Wolfe
  * Justin Braben
  * Maciej 'vesim' Kuliński
  * Nico Elbers
  * Parzival-3141
  * Sashko
  * andrewkraevskii
  * gooncreeper
  * nikneym
  * rpkak
  * saurabh
  * schtvn
  * Adheesh Wadkar
  * Aikawa Yataro
  * Benjamin Thompson
  * Bogdan Romanyuk
  * Des-Nerger
  * Felix "xq" Queißner
  * Francesco Alemanno
  * Gabriel Borrelli
  * GalaxyShard
  * JonathanHallstrom
  * Karol Kosek
  * Ketan Reynolds
  * Liam Swayne
  * Luuk de Gram
  * Mario Nachbaur
  * Mason Remaley
  * Nguyễn Gia Phong
  * PauloCampana
  * Pierre Tachoire
  * Reuben Dunnington
  * Scott Redig
  * Stephen Gregoratto
  * Travis Lange
  * Travis Staloch
  * Tristan Ross
  * Yusuf Bham
  * axel escalada
  * bilaliscarioth
  * gooncreeper
  * ippsav
  * kj4tmp
  * pfg
  * poypoyan
  * rohlem
  * sobolevn
  * thejohnny5
  * xtex
  * 87
  * Alec Fessler
  * Alex Ambrose
  * Aman Karmani
  * Anders Bondehagen
  * Andrew Barchuk
  * Archbirdplus
  * Archit Gupta
  * Arwalk
  * Ben Grant
  * Benjamin
  * Benjamin Hetz
  * Bing Sun
  * Bingwu Zhang
  * Bob Farrell
  * Brad Olson
  * Bram
  * Brian Cain
  * Brook Jeynes
  * Bruno Franca dos Reis
  * Bruno Reis
  * Bryce Vandegrift
  * Cheng Sheng
  * Chris Covington
  * Christian Fillion
  * CrazyboyQCD
  * Daniel Berg
  * Devin J. Pohly
  * Don
  * DravenK
  * Ekin Dursun
  * Enrique Miguel Mora Meza
  * Eric Petersen
  * Erik Arvstedt
  * Eugene-Dash
  * ExeVirus
  * Fabio Arnold
  * Fausto Ribeiro
  * Federico Di Pierro
  * Forest
  * Frank Plowman
  * Gabor Lekeny
  * Gordon Cassie
  * Guillaume Wenzek
  * Harrison McCarty
  * Hayden Riddiford
  * Hila Friedman
  * Igor Stojković
  * Ilia Choly
  * InKryption
  * Jakub Dóka
  * Jan Hendrik Farr
  * Jean-Baptiste "Jiboo" Lepesme
  * Jeffrey C. Ollie
  * Jesse Wattenbarger
  * Jonathan Hallstrom
  * Jora Troosh
  * José M Rico
  * Juan Julián Merelo Guervós
  * Julian Noble
  * Julian Vesper
  * KNnut
  * Kamil T
  * Karim Mk
  * Kiëd Llaentenn
  * Kouosi Takayama
  * Kyle Schwarz
  * L zard
  * LiterallyVoid
  * LmanTW
  * Manuel Spagnolo
  * Mark Rushakoff
  * Matthew Ettler
  * Meili C
  * Michael Lynch
  * Michael Ortmann
  * Michał Drozd
  * Misaki Kasumi
  * Mohanavel S K
  * MrDmitry
  * Nameless
  * Nelson Crosby
  * Nikita
  * PauloCampana
  * Peng Guanwen
  * Prokop Randáček
  * Raed Rizqie
  * Rafael Batiati
  * Rich Remer
  * Rohan Vashisht
  * Roman Frołow
  * Rui He
  * Ryan G
  * Ryan Sepassi
  * Sammy James
  * Samuel Fiedler
  * Sean
  * Shane Peelar
  * Shawn Gao
  * Simon Ekström
  * T
  * Tangtang Zhou
  * ThisPC
  * Vahur Sinijärv
  * Vesim
  * Wayne Wu
  * Wyatt Radkiewicz
  * bing
  * bsubei
  * cancername
  * cdeler
  * cheme
  * cryptocode
  * curuvar
  * dave caruso
  * dbubel
  * eric-saintetienne
  * expikr
  * fdfdjfk3
  * fmaggi
  * fn ⌃ ⌥
  * gabeuehlein
  * gbaraldi
  * geemili
  * injuly
  * ippsav
  * isaac yonemoto
  * llogick
  * matt
  * matt ettler
  * max
  * melonedo
  * nobkd
  * pseudoc
  * reokodoku
  * saccharin
  * sidharta
  * sin-ack
  * snoire
  * ssmid
  * tgschultz
  * zhylmzr
  * ziggoon

## Thank You Sponsors! §

![Ziggy the Ziguana](https://ziglang.org/img/Ziggy_6.svg)

Special thanks to those who [sponsor Zig](/zsf/). Because of recurring
donations, Zig is driven by the open source community, rather than the goal of
making profit. In particular, these fine folks sponsor Zig for $50/month or
more:

  * [Josh Wolfe](https://github.com/thejoshwolfe)
  * [Matt Knight](https://mattnite.net)
  * [Stevie Hryciw](https://www.hryx.net/)
  * [Jethro Nederhof](https://jethron.id.au)
  * [Karrick McDermott](https://hachyderm.io/@karrick)
  * [José M Rico](https://www.kapricornmedia.com)
  * [drfuchs](https://github.com/drfuchs)
  * [Joran Dirk Greef](https://github.com/tigerbeetle/tigerbeetle)
  * [Rui Ueyama](https://github.com/rui314)
  * [bfredl](https://github.com/bfredl)
  * [Simon A. Nielsen Knights](https://codeberg.org/tauoverpi/)
  * [Emi](https://emidoots.com)
  * [Derek Collison](https://derekcollison.net)
  * [Daniele Cocca](https://github.com/jmc-88)
  * [Rafael Batiati](https://twitter.com/rbatiati)
  * [Aras Pranckevičius](https://aras-p.info)
  * [Terin Stock](https://terinstock.com)
  * [Loïc Tosser](https://kalvad.com)
  * [Kirk Scheibelhut](https://scheibo.com)
  * [Brian Gold](https://github.com/briangold)
  * [Paul Harrington](https://github.com/phrrngtn)
  * [Clark Gaebel](https://github.com/cgaebel)
  * [Bun](https://bun.sh/)
  * [Marcus Eagan](https://www.marcus.art/)
  * [Ken Chilton](https://www.chilton-consulting.com)
  * [Will Manning](https://twitter.com/_willmanning)
  * [Spiral](https://spiraldb.com)
  * [Alex Mackenzie at Tapestry VC](https://mack.work)
  * [Leo Razoumov](https://github.com/slonik-az)
  * [Alok Parlikar](http://www.parlikar.com)
  * [Viktor Tratsevskyy](https://www.horster.org)
  * [Huly® Platform™](https://huly.io)
  * [Keygen](https://keygen.sh)
  * Reuben Dunnington
  * Isaac Yonemoto
  * Auguste Rame
  * Jay Petacat
  * Dirk de Visser
  * Santiago Andaluz
  * Andrew Mangogna
  * Yaroslav Zhavoronkov
  * Chris Heyes
  * James McGill
  * Luke Champine
  * AG.王爱国
  * Wojtek Mach
  * Daniel Hensley
  * Erik Mållberg
  * Christopher Dolan
  * Fabio Arnold
  * Ross Rheingans-Yoo
  * Justin "J.R." Hill
  * 🇺🇦 Mykhailo Tsiuptsiun
  * Kiril Mihaylov
  * Brett Slatkin
  * Sean Carey
  * Yurii Rashkovskii
  * OM PropTech GmbH
  * Lucas
  * Alex Sergeev
  * Josh Ashby
  * Chris Baldwin
  * Malcolm Still
  * Francis Bouvier
  * Nathan Bourgeois
  * Fawzi Mohamed
  * Ian Johnson
  * Carlos Pizano Uribe
  * Anita SV
  * Rene Schallner
  * Jinkyu Yi
  * Jake Hemmerle
  * Will Pragnell
  * Peter Snelgrove
  * Jeff Fowler
  * Christian Gibson
  * Kohei Nozaki
  * Dylan Conway
  * Hlib Kanunnikov
  * Miguel Filipe
  * merkleplant
  * Duncan Marsh
  * Nikolay Govorov
  * Roast Beef Kazenzakis
  * Willian Hasse
  * daily.dev
  * Sonic
  * Matteo De Wint
  * FumingPower
  * Matteias Collet
  * smallkirby
  * Stefan Hagen
  * Miles J McGruder
  * Álvaro Justen
  * Laaman03
  * Paul Horn

