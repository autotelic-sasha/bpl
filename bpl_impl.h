#pragma once

#include <map>
#include <string>
#include <memory>

namespace autotelica {
    class bpl_impl;

    class bpl {
        std::shared_ptr<bpl_impl> _impl;
    public:
        bpl(
            std::string const& source_path_,
            std::string const& target_path_,
            std::string const& config_path_,
            bool strict_ = false,
            std::string const& extensions_to_ignore_ = "",
            std::string const& files_to_ignore_ = "");
        
        bpl(
            std::string const& source_path_,
            std::string const& target_path_,
            bool strict_ = false,
            std::string const& extensions_to_ignore_ = "",
            std::string const& files_to_ignore_ = "",
            std::map<std::string, std::string> const& kvm_ = {});

        bpl(
            std::string const& source_path_,
            std::string const& target_path_,
            bool strict_ = false,
            std::string const& extensions_to_ignore_ = "",
            std::string const& files_to_ignore_ = "",
            std::string const& named_values_s = "");


        // generating projects from templates
        void generate();

        // generating blank configuration files
        // then you just populate them with values,it's nice
        void generate_config_files();

        // got a new template to deal with? 
        // or one that you wrote but forgot all about?
        // use 'describe' to get information about it on screen.
        void describe();

    };
}