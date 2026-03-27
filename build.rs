// Confidential Information of Motphys. Not for disclosure or distribution without Motphys's prior
// written consent.
//
// This software contains code, techniques and know-how which is confidential and proprietary to
// Motphys.
//
// Product and Trade Secret source code contains trade secrets of Motphys.
//
// Copyright (C) 2020-2024 Motphys Technology Co., Ltd. All Rights Reserved.
//
// This software belongs to the Intellectual Property of Motphys. Use of this software is subject to
// the terms and conditions in the license file accompanying. You may not use this software except
// in compliance with the license file.

use std::path::PathBuf;
use std::process::Command;

fn main() {
    // Only run gen-mjcf-md during release builds with a feature flag
    if cfg!(feature = "run-doc-gen") {
        println!("cargo:rerun-if-changed=../../mjcf-parser/src");
        println!("cargo:warning=Running xtask gen-mjcf-md...");

        // Get the workspace root directory
        let manifest_dir = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR").unwrap());

        // From motrixsim-oni/motrixsim-py, go up 2 levels to reach workspace root
        let workspace_root = manifest_dir.parent().and_then(|p| p.parent()).unwrap();

        // Try to use the debug xtask binary first (faster, likely already built)
        let debug_xtask = workspace_root.join("target/debug/xtask");

        let xtask_binary = if debug_xtask.exists() {
            debug_xtask
        } else {
            // Fall back to release binary
            workspace_root.join("target/release/xtask")
        };

        if xtask_binary.exists() {
            let output = Command::new(&xtask_binary)
                .args([
                    "gen-mjcf-md",
                    "--input-dir",
                    &workspace_root.join("mjcf-parser/src").to_string_lossy(),
                    "--output-dir",
                    &workspace_root
                        .join("motrixsim-oni/motrixsim-py/docs/source/_shared/user_guide/getting_started")
                        .to_string_lossy(),
                ])
                .output();

            match output {
                Ok(output) => {
                    if output.status.success() {
                        println!("{}", String::from_utf8_lossy(&output.stdout));
                    } else {
                        let stderr = String::from_utf8_lossy(&output.stderr);
                        let stdout = String::from_utf8_lossy(&output.stdout);
                        println!(
                            "cargo:warning=xtask gen-mjcf-md failed:\nstdout:\n{}\nstderr:\n{}",
                            stdout, stderr
                        );
                    }
                }
                Err(e) => {
                    println!("cargo:warning=Failed to run xtask gen-mjcf-md: {}", e);
                }
            }
        } else {
            println!(
                "cargo:warning=xtask binary not found at {:?}. Run 'cargo xtask gen-mjcf-md' manually.",
                xtask_binary
            );
        }
    }
}
